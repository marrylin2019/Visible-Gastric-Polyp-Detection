"""
@Project ：Graduation-Project-Fluent 
@File    ：datasetypes.py
@Author  ：X0RB64
@Date    ：2023/03/25 16:50 
"""
from enum import Enum

from yolosegmention.exceptions import RuntimeException


class DatasetTypes(Enum):
    KVASIR_SEG = 0
    UNETPP = 1
    YOLOv8 = 2
    YOLOv7 = 3
    YOLOv5 = 4

    @staticmethod
    def str(datasetType: Enum):
        if datasetType.value == DatasetTypes.KVASIR_SEG.value:
            return 'Kvasir-SEG'
        elif datasetType.value == DatasetTypes.UNETPP.value:
            return 'Unet++'
        elif datasetType.value == DatasetTypes.YOLOv8.value:
            return 'YOLOv8'
        elif datasetType.value == DatasetTypes.YOLOv7.value:
            return 'YOLOv7'
        elif datasetType.value == DatasetTypes.YOLOv5.value:
            return 'YOLOv5'
        else:
            raise RuntimeException('未覆盖的数据集！')

    @staticmethod
    def enumInt(value: int):
        if value == 0:
            return DatasetTypes.KVASIR_SEG
        elif value == 1:
            return DatasetTypes.UNETPP
        elif value == 2:
            return DatasetTypes.YOLOv8
        elif value == 3:
            return DatasetTypes.YOLOv7
        elif value == 4:
            return DatasetTypes.YOLOv5
        else:
            raise RuntimeException('未覆盖的数据集！')

    @staticmethod
    def enumStr(value: str):
        if value == 'Kvasir-SEG':
            return DatasetTypes.KVASIR_SEG
        elif value == 'Unet++':
            return DatasetTypes.UNETPP
        elif value == 'YOLOv8':
            return DatasetTypes.YOLOv8
        elif value == 'YOLOv7':
            return DatasetTypes.YOLOv7
        elif value == 'YOLOv5':
            return DatasetTypes.YOLOv5
        else:
            raise RuntimeException('未覆盖的数据集！')

    @staticmethod
    def strList():
        return [DatasetTypes.str(DatasetTypes.enumInt(i)) for i in range(5)]