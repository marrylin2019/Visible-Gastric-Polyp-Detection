"""
@Project ：Graduation-Project-Fluent
@File    ：slice.py
@Author  ：X0RB64
@Date    ：2023/03/24 14:57
"""

import math
import random

from .utils import standardise_file_name


class Slicer:
    """
    随机划分测试集与数据集
    比例：
        Train：Val = 70% : 30%
    """
    def __init__(self, names: list[str]):
        """
        :param names: 文件名列表
        """
        # 初始化
        self.__file_names = dict()
        self.__file_names['val'] = list()
        self.__file_names['train'] = list()
        self.__file_names['raw'] = names

        self.__standardise()
        self.__slice()

    def __standardise(self):
        for i in range(len(self.__file_names['raw'])):
            self.__file_names['raw'][i] = standardise_file_name(self.__file_names['raw'][i])

    def __slice(self):
        random.shuffle(self.__file_names['raw'])
        position = math.ceil(len(self.__file_names['raw']) * 0.7)
        self.__file_names['train'] = self.__file_names['raw'][:position]
        self.__file_names['val'] = self.__file_names['raw'][position:]

    @property
    def train_set(self) -> list[str]:
        return self.__file_names['train']

    @property
    def val_set(self) -> list[str]:
        return self.__file_names['val']
