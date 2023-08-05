import argparse
import json
import os
from pathlib import Path
from threading import Thread

import numpy as np
import torch
import yaml
from tqdm import tqdm

from yolov5.helpers import OptFactory
from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import create_dataloader
from yolov5.utils.general import (box_iou, check_dataset, check_file,
                                  check_img_size, coco80_to_coco91_class,
                                  increment_path, non_max_suppression,
                                  scale_coords, set_logging, xywh2xyxy,
                                  xyxy2xywh)
from yolov5.utils.loss import compute_loss
from yolov5.utils.metrics import ConfusionMatrix, ap_per_class
from yolov5.utils.plots import output_to_target, plot_images, plot_study_txt
from yolov5.utils.torch_utils import select_device, time_synchronized


def test(
    weights=None,
    data="yolov5/data/coco128.yaml",
    batch_size=32,
    image_size=640,
    conf_thres=0.001,
    iou_thres=0.6,  # for NMS
    task="val",
    device="",
    single_cls=False,
    augment=False,
    verbose=False,
    save_txt=False,  # for auto-labelling
    save_hybrid=False,  # for hybrid auto-labelling
    save_conf=False,  # save auto-label confidences
    save_json=False,
    project="runs/test",
    name="exp",
    exist_ok=False,
    model=None,
    dataloader=None,
    save_dir=Path(""),  # for saving images
    plots=True,
    log_imgs=0,  # number of logged images
):
    arguments = locals()
    # Initialize/load model and set device
    training = model is not None
    if training:  # called by train.py
        device = next(model.parameters()).device  # get model device

    else:  # called directly
        set_logging()
        device = select_device(device, batch_size=batch_size)

        # Directories
        save_dir = Path(
            increment_path(Path(project) / name, exist_ok=exist_ok)
        )  # increment run
        (save_dir / "labels" if save_txt else save_dir).mkdir(
            parents=True, exist_ok=True
        )  # make dir

        # Load model
        model = attempt_load(weights, map_location=device)  # load FP32 model
        image_size = check_img_size(image_size, s=model.stride.max())  # check img_size

        # Multi-GPU disabled, incompatible with .half() https://github.com/ultralytics/yolov5/issues/99
        # if device.type != 'cpu' and torch.cuda.device_count() > 1:
        #     model = nn.DataParallel(model)

    # Half
    half = device.type != "cpu"  # half precision only supported on CUDA
    if half:
        model.half()

    # Configure
    model.eval()
    is_coco = data.endswith("coco.yaml")  # is COCO dataset
    with open(data) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)  # model dict
    check_dataset(data)  # check
    nc = 1 if single_cls else int(data["nc"])  # number of classes
    iouv = torch.linspace(0.5, 0.95, 10).to(device)  # iou vector for mAP@0.5:0.95
    niou = iouv.numel()

    # Logging
    log_imgs, wandb = min(log_imgs, 100), None  # ceil
    try:
        import wandb  # Weights & Biases
    except ImportError:
        log_imgs = 0

    # Dataloader
    if not training:
        img = torch.zeros((1, 3, image_size, image_size), device=device)  # init img
        _ = (
            model(img.half() if half else img) if device.type != "cpu" else None
        )  # run once
        path = (
            data["test"] if task == "test" else data["val"]
        )  # path to val/test images
        opt = OptFactory(arguments)
        dataloader = create_dataloader(
            path, image_size, batch_size, model.stride.max(), opt, pad=0.5, rect=True
        )[0]

    seen = 0
    confusion_matrix = ConfusionMatrix(nc=nc)
    names = {
        k: v
        for k, v in enumerate(
            model.names if hasattr(model, "names") else model.module.names
        )
    }
    coco91class = coco80_to_coco91_class()
    s = ("%20s" + "%12s" * 6) % (
        "Class",
        "Images",
        "Targets",
        "P",
        "R",
        "mAP@.5",
        "mAP@.5:.95",
    )
    p, r, f1, mp, mr, map50, map, t0, t1 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    loss = torch.zeros(3, device=device)
    jdict, stats, ap, ap_class, wandb_images = [], [], [], [], []
    for batch_i, (img, targets, paths, shapes) in enumerate(tqdm(dataloader, desc=s)):
        img = img.to(device, non_blocking=True)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        targets = targets.to(device)
        nb, _, height, width = img.shape  # batch size, channels, height, width

        with torch.no_grad():
            # Run model
            t = time_synchronized()
            inf_out, train_out = model(
                img, augment=augment
            )  # inference and training outputs
            t0 += time_synchronized() - t

            # Compute loss
            if training:
                loss += compute_loss([x.float() for x in train_out], targets, model)[1][
                    :3
                ]  # box, obj, cls

            # Run NMS
            targets[:, 2:] *= torch.Tensor([width, height, width, height]).to(
                device
            )  # to pixels
            lb = (
                [targets[targets[:, 0] == i, 1:] for i in range(nb)]
                if save_hybrid
                else []
            )  # for autolabelling
            t = time_synchronized()
            output = non_max_suppression(
                inf_out, conf_thres=conf_thres, iou_thres=iou_thres, labels=lb
            )
            t1 += time_synchronized() - t

        # Statistics per image
        for si, pred in enumerate(output):
            labels = targets[targets[:, 0] == si, 1:]
            nl = len(labels)
            tcls = labels[:, 0].tolist() if nl else []  # target class
            path = Path(paths[si])
            seen += 1

            if len(pred) == 0:
                if nl:
                    stats.append(
                        (
                            torch.zeros(0, niou, dtype=torch.bool),
                            torch.Tensor(),
                            torch.Tensor(),
                            tcls,
                        )
                    )
                continue

            # Predictions
            predn = pred.clone()
            scale_coords(
                img[si].shape[1:], predn[:, :4], shapes[si][0], shapes[si][1]
            )  # native-space pred

            # Append to text file
            if save_txt:
                gn = torch.tensor(shapes[si][0])[
                    [1, 0, 1, 0]
                ]  # normalization gain whwh
                for *xyxy, conf, cls in predn.tolist():
                    xywh = (
                        (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn)
                        .view(-1)
                        .tolist()
                    )  # normalized xywh
                    line = (
                        (cls, *xywh, conf) if save_conf else (cls, *xywh)
                    )  # label format
                    with open(save_dir / "labels" / (path.stem + ".txt"), "a") as f:
                        f.write(("%g " * len(line)).rstrip() % line + "\n")

            # W&B logging
            if plots and len(wandb_images) < log_imgs:
                box_data = [
                    {
                        "position": {
                            "minX": xyxy[0],
                            "minY": xyxy[1],
                            "maxX": xyxy[2],
                            "maxY": xyxy[3],
                        },
                        "class_id": int(cls),
                        "box_caption": "%s %.3f" % (names[cls], conf),
                        "scores": {"class_score": conf},
                        "domain": "pixel",
                    }
                    for *xyxy, conf, cls in pred.tolist()
                ]
                boxes = {
                    "predictions": {"box_data": box_data, "class_labels": names}
                }  # inference-space
                wandb_images.append(
                    wandb.Image(img[si], boxes=boxes, caption=path.name)
                )

            # Append to pycocotools JSON dictionary
            if save_json:
                # [{"image_id": 42, "category_id": 18, "bbox": [258.15, 41.29, 348.26, 243.78], "score": 0.236}, ...
                image_id = int(path.stem) if path.stem.isnumeric() else path.stem
                box = xyxy2xywh(predn[:, :4])  # xywh
                box[:, :2] -= box[:, 2:] / 2  # xy center to top-left corner
                for p, b in zip(pred.tolist(), box.tolist()):
                    jdict.append(
                        {
                            "image_id": image_id,
                            "category_id": coco91class[int(p[5])]
                            if is_coco
                            else int(p[5]),
                            "bbox": [round(x, 3) for x in b],
                            "score": round(p[4], 5),
                        }
                    )

            # Assign all predictions as incorrect
            correct = torch.zeros(pred.shape[0], niou, dtype=torch.bool, device=device)
            if nl:
                detected = []  # target indices
                tcls_tensor = labels[:, 0]

                # target boxes
                tbox = xywh2xyxy(labels[:, 1:5])
                scale_coords(
                    img[si].shape[1:], tbox, shapes[si][0], shapes[si][1]
                )  # native-space labels
                if plots:
                    confusion_matrix.process_batch(
                        pred, torch.cat((labels[:, 0:1], tbox), 1)
                    )

                # Per target class
                for cls in torch.unique(tcls_tensor):
                    ti = (
                        (cls == tcls_tensor).nonzero(as_tuple=False).view(-1)
                    )  # prediction indices
                    pi = (
                        (cls == pred[:, 5]).nonzero(as_tuple=False).view(-1)
                    )  # target indices

                    # Search for detections
                    if pi.shape[0]:
                        # Prediction to target ious
                        ious, i = box_iou(predn[pi, :4], tbox[ti]).max(
                            1
                        )  # best ious, indices

                        # Append detections
                        detected_set = set()
                        for j in (ious > iouv[0]).nonzero(as_tuple=False):
                            d = ti[i[j]]  # detected target
                            if d.item() not in detected_set:
                                detected_set.add(d.item())
                                detected.append(d)
                                correct[pi[j]] = ious[j] > iouv  # iou_thres is 1xn
                                if (
                                    len(detected) == nl
                                ):  # all targets already located in image
                                    break

            # Append statistics (correct, conf, pcls, tcls)
            stats.append((correct.cpu(), pred[:, 4].cpu(), pred[:, 5].cpu(), tcls))

        # Plot images
        if plots and batch_i < 3:
            f = save_dir / f"test_batch{batch_i}_labels.jpg"  # labels
            Thread(
                target=plot_images, args=(img, targets, paths, f, names), daemon=True
            ).start()
            f = save_dir / f"test_batch{batch_i}_pred.jpg"  # predictions
            Thread(
                target=plot_images,
                args=(img, output_to_target(output), paths, f, names),
                daemon=True,
            ).start()

    # Compute statistics
    stats = [np.concatenate(x, 0) for x in zip(*stats)]  # to numpy
    if len(stats) and stats[0].any():
        p, r, ap, f1, ap_class = ap_per_class(
            *stats, plot=plots, save_dir=save_dir, names=names
        )
        p, r, ap50, ap = (
            p[:, 0],
            r[:, 0],
            ap[:, 0],
            ap.mean(1),
        )  # [P, R, AP@0.5, AP@0.5:0.95]
        mp, mr, map50, map = p.mean(), r.mean(), ap50.mean(), ap.mean()
        nt = np.bincount(
            stats[3].astype(np.int64), minlength=nc
        )  # number of targets per class
    else:
        nt = torch.zeros(1)

    # Print results
    pf = "%20s" + "%12.3g" * 6  # print format
    print(pf % ("all", seen, nt.sum(), mp, mr, map50, map))

    # Print results per class
    if verbose and nc > 1 and len(stats):
        for i, c in enumerate(ap_class):
            print(pf % (names[c], seen, nt[c], p[i], r[i], ap50[i], ap[i]))

    # Print speeds
    t = tuple(x / seen * 1e3 for x in (t0, t1, t0 + t1)) + (
        image_size,
        image_size,
        batch_size,
    )  # tuple
    if not training:
        print(
            "Speed: %.1f/%.1f/%.1f ms inference/NMS/total per %gx%g image at batch-size %g"
            % t
        )

    # Plots
    if plots:
        confusion_matrix.plot(save_dir=save_dir, names=list(names.values()))
        if wandb and wandb.run:
            wandb.log({"Images": wandb_images})
            wandb.log(
                {
                    "Validation": [
                        wandb.Image(str(f), caption=f.name)
                        for f in sorted(save_dir.glob("test*.jpg"))
                    ]
                }
            )

    # Save JSON
    if save_json and len(jdict):
        w = (
            Path(weights[0] if isinstance(weights, list) else weights).stem
            if weights is not None
            else ""
        )  # weights
        anno_json = "../coco/annotations/instances_val2017.json"  # annotations json
        pred_json = str(save_dir / f"{w}_predictions.json")  # predictions json
        print("\nEvaluating pycocotools mAP... saving %s..." % pred_json)
        with open(pred_json, "w") as f:
            json.dump(jdict, f)

        try:  # https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoEvalDemo.ipynb
            from pycocotools.coco import COCO
            from pycocotools.cocoeval import COCOeval

            anno = COCO(anno_json)  # init annotations api
            pred = anno.loadRes(pred_json)  # init predictions api
            eval = COCOeval(anno, pred, "bbox")
            if is_coco:
                eval.params.imgIds = [
                    int(Path(x).stem) for x in dataloader.dataset.img_files
                ]  # image IDs to evaluate
            eval.evaluate()
            eval.accumulate()
            eval.summarize()
            map, map50 = eval.stats[:2]  # update results (mAP@0.5:0.95, mAP@0.5)
        except Exception as e:
            print(f"pycocotools unable to run: {e}")

    # Return results
    if not training:
        s = (
            f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}"
            if save_txt
            else ""
        )
        print(f"Results saved to {save_dir}{s}")
    model.float()  # for training
    maps = np.zeros(nc) + map
    for i, c in enumerate(ap_class):
        maps[c] = ap[i]
    return (mp, mr, map50, map, *(loss.cpu() / len(dataloader)).tolist()), maps, t
