"""
@Project ：GraduationProject 
@File    ：TrainModelUI.py
@Author  ：X0RB64
@Date    ：2023/02/19 19:53 
"""
import os.path

from yolosegmention.exceptions import RuntimeException
from ...dataset.preprocess.common import check
from ultralytics import YOLO
from yolosegmention.beans import DatasetTypes


def train(preWeight_path: str, dataset_path: str, task: str = 'segment', epochs: int = 10, batch: int = 16, imgsiz: int = 640) -> None:
    """
    :param preWeight_path: 预训练权重文件，.pt或yaml
    :param dataset_path: 数据集配置文件，.yaml
    :param task: 任务模式，segment/detection/classification
    :param epochs: 训练轮次
    :param batch: 同时训练的图片数量
    :param imgsiz: 图片尺寸
    """
    #  首先验证数据集是否完整
    checkRes = check(dataset_path, DatasetTypes.YOLOv8)
    if not checkRes[0]:
        raise RuntimeException(checkRes[1])

    # Load a model
    model = YOLO(os.path.abspath(preWeight_path))  # build a new model from scratch

    # Train the model
    results = model.train(data=os.path.abspath(dataset_path), task=task, epochs=epochs, batch=batch, imgsz=imgsiz)
    model.val()


if __name__ == '__main__':
    train(preWeight_path=r'D:\Program\Python\Graduation-Project-Fluent\yolosegmention\core\models\yolov8\pre-weights\best.pt', dataset_path='../../../data/dataset/dataset.yaml', epochs=1)
