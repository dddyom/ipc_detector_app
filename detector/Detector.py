import matplotlib.pyplot as plt

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo

import cv2
from os.path import dirname, join
from detectron2.data.datasets import register_coco_instances

register_coco_instances("_train", {}, "./coco_dataset/train/_annotations.coco.json", "./coco_dataset/train")
register_coco_instances("_val", {}, "./coco_dataset/valid/_annotations.coco.json", "./coco_dataset/valid")
register_coco_instances("_test", {}, "./coco_dataset/test/_annotations.coco.json", "./coco_dataset/test")

from detectron2.data import MetadataCatalog
MetadataCatalog.get("_train").thing_classes = ["sigal", "stray", "target"]
MetadataCatalog.get("_val").thing_classes = ["sigal", "stray", "target"]
MetadataCatalog.get("_test").thing_classes = ["sigal", "stray", "target"]

class Detector:
    def __init__(self, model_type="OD") -> None:
        self.cfg = get_cfg()
        if model_type == "OD":
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = str(join(dirname(__file__), "weights/model_final.pth"))
            self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3

        elif model_type == "IS":
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.cfg.MODEL.DEVICE = "cpu"
        self.cfg.DATASETS.TRAIN = ("_train",)
        self.cfg.DATASETS.TEST = ("_val",)
        

        self.predictor = DefaultPredictor(self.cfg)

    def onImage(self, imagePath):
        image0 = cv2.imread(imagePath)
        image = cv2.resize(image0, (256, 240)) 
        predictions = self.predictor(image)


        category_id = predictions['instances'].get("pred_classes").numpy()
        
        if 2 in category_id:

            pred_boxes = []
            coordinates = []
            for i in range(len(category_id)):
                if category_id[i] == 2:
                    pred_boxes.append(predictions["instances"].pred_boxes.tensor.numpy()[i])
            for j in pred_boxes:
                coordinates.append(Detector.BoxCenter(j))
            return coordinates
    
    @staticmethod 
    def BoxCenter(box_coordinates):
        x1, x2, y1, y2 = box_coordinates[0], box_coordinates[2], box_coordinates[1], box_coordinates[2]
        return (x1 + x2) / 2, (y1 + y2) / 2

