"""
@Project ：Graduation-Project-Fluent 
@File    ：dataset_model_types.py
@Author  ：X0RB64
@Date    ：2023/03/25 16:50 
"""
from enum import Enum


class DatasetTypes(Enum):
    KVASIR_SEG = 'Kvasir-SEG'
    UNETPP = 'Unet++'
    YOLOv8 = 'YOLOv8'
    YOLOv7 = 'YOLOv7'
    YOLOv5 = 'YOLOv5'


class ModelTypes(Enum):
    YOLOv8_SEGMENT = 'YOLOv8-Segment'
    YOLOv8_DETECTION = 'YOLOv8-Detection'
    UNETPP = 'UNet++'
    YOLOv7_DETECTION = 'YOLOv7-Detection'
    YOLOv5_DETECTION = 'YOLOv5-Detection'


def model2types(model: ModelTypes):
    return {
        ModelTypes.YOLOv8_SEGMENT: DatasetTypes.YOLOv8,
        ModelTypes.YOLOv8_DETECTION: DatasetTypes.YOLOv8,
        ModelTypes.UNETPP: DatasetTypes.UNETPP,
        ModelTypes.YOLOv7_DETECTION: DatasetTypes.YOLOv7,
        ModelTypes.YOLOv5_DETECTION: DatasetTypes.YOLOv5,
    }[model]
