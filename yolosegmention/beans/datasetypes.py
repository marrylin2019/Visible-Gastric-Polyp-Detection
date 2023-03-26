"""
@Project ：Graduation-Project-Fluent 
@File    ：datasetypes.py
@Author  ：X0RB64
@Date    ：2023/03/25 16:50 
"""
from enum import Enum


class DatasetTypes(Enum):
    KVASIR_SEG = 0
    UNETPP = 1
    YOLOv8 = 2
    YOLOv7 = 3
    YOLOv5 = 4
