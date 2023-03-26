"""
@Project ：GraduationProject 
@File    ：PredictUI.py
@Author  ：X0RB64
@Date    ：2023/03/19 21:51 
"""
import re

import cv2
from Code.Core.ultralytics import YOLO
from Code.Beans.StreamTypes import TYPES, PATTERNS
from Code.Beans import Exit


def predict(_type: str, path: str, pre_weights_path: str):
    if _type not in TYPES:
        Exit.exit_process(Exit.UNREACHABLE_ERR)
    if re.match(PATTERNS[_type], path) is None:
        Exit.exit_process(Exit.UNREACHABLE_ERR)
    if _type == TYPES[0]:
        predictImg(path, pre_weights_path)
        pass
    elif _type == TYPES[1]:
        predictVideo()
        pass
    elif _type == TYPES[2]:
        predictStream()
        pass
    pass


def predictImg(imgPath: str, pre_weights_path: str):
    img = cv2.imread(imgPath)
    model = YOLO(pre_weights_path)
    results = model.predict(source=img, save=True)
    pass


def predictVideo():
    pass


def predictStream():
    pass


if __name__ == '__main__':
    predict('图片', r'D:\Program\GraduationProject\data\segmented-images\images\0b556d02-f9ca-4270-b568-3200335c7d08.png',
            './pre-weights/best.pt')
