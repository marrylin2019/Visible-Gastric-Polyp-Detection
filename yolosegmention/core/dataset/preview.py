"""
@Project ：Graduation-Project-Fluent 
@File    ：preview.py
@Author  ：X0RB64
@Date    ：2023/03/26 16:16 
"""
import os
import shutil

import cv2
import random
import numpy as np


def show(pic_path, txt_path, color_map: dict[str: tuple[int, int, int]]):
    img = cv2.imread(pic_path)
    height, width, _ = img.shape
    file_handle = open(txt_path)
    cnt_info = file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]
    for new_info in new_cnt_info:
        s = []
        for i in range(1, len(new_info), 2):
            b = [float(tmp) for tmp in new_info[i:i + 2]]
            s.append([int(b[0] * width), int(b[1] * height)])
        zeros = np.zeros(img.shape, dtype=np.uint8)
        mask = cv2.fillPoly(zeros, [np.array(s, np.int32)], color=color_map.get(new_info[0]))
        img = 0.9 * mask + img
        # cv2.polylines(img, [np.array(s, np.int32)], True, color_map.get(new_info[0]))
    return img


def generate(pic_path: str, txt_path: str, res_path, num: int, color_map: dict[str: tuple[int, int, int]]):
    """
    :param pic_path: 掩膜图片根路径
    :param txt_path: 标注文件根路径
    :param res_path: 结果文件根路径
    :param num:      测试图片数量
    :param color_map: 颜色集合，形如{type: (R, G, B)}
    """
    if os.path.exists(res_path):
        shutil.rmtree(res_path)
    os.mkdir(res_path)
    names = [name[:-4] for name in os.listdir(txt_path)]
    random.shuffle(names)
    for i in range(num):
        final_pic_path = os.path.join(pic_path, names[i] + '.png')
        final_txt_path = os.path.join(txt_path, names[i] + '.txt')
        final_res_path = os.path.join(res_path, names[i] + '.png')
        cv2.imwrite(final_res_path, show(final_pic_path, final_txt_path, color_map))
