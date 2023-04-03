"""
@Project ：GraduationProject 
@File    ：PredictUI.py
@Author  ：X0RB64
@Date    ：2023/03/19 21:51 
"""
import re
from pathlib import Path

import cv2
from ultralytics import YOLO

from yolosegmention.beans import StreamTypes, PATTERNS
from yolosegmention.exceptions import RuntimeException


def predict(_type: str, path: str, pre_weights_path: str):
    try:
        _type = StreamTypes(_type)
    except ValueError:
        raise RuntimeException(f'{_type}是非法的数据类型！')
    else:
        if re.match(PATTERNS[_type], path) is None:
            raise RuntimeException(f'{path}格式不合法！')
        if _type == StreamTypes.PICTURE:
            predictImg(path, pre_weights_path)
            pass
        elif _type == StreamTypes.VIDEO:
            predictVideo(path, pre_weights_path)
            pass
        elif _type == StreamTypes.STREAM:
            predictStream()
            pass
        pass


def predictImg(imgPath: str, pre_weights_path: str):
    img = cv2.imread(imgPath)
    model = YOLO(pre_weights_path)
    results = model.predict(source=img, save=True)
    pass


def predictVideo(videoPath: str, pre_weights_path: str):
    model = YOLO(pre_weights_path)
    results = model.predict(source=videoPath, save=True)
    pass


def predictStream():
    pass
