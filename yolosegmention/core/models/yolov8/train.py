"""
@Project ：GraduationProject 
@File    ：TrainModelUI.py
@Author  ：X0RB64
@Date    ：2023/02/19 19:53 
"""
import os.path

from ...dataset.preprocess.common import check
from yolosegmention.libs import YOLO
from yolosegmention.beans import DatasetTypes


def train(model_path: str, dataset_path: str, task: str = 'segment', epochs: int = 10, batch: int = 16, imgsiz: int = 640):
    """ 谁调用就在哪生成runs文件夹 """
    #  首先验证数据集是否完整
    checkRes = check(dataset_path, DatasetTypes.YOLOv8)
    # Load a model
    model = YOLO(os.path.abspath(model_path))  # build a new model from scratch

    # Train the model
    results = model.train(data=os.path.abspath(dataset_path), task=task, epochs=epochs, batch=batch, imgsz=imgsiz)
    model.val()


if __name__ == '__main__':
    train(model_path=r'./pre-weights/yolov8n-seg.pt', dataset_path='../../../data/dataset/dataset.yaml', epochs=1)
