"""
@Project ：Graduation-Project-Fluent 
@File    ：kvasir_seg.py
@Author  ：X0RB64
@Date    ：2023/03/24 15:12 
"""
import json
import os.path

from .base import BaseGetter
from ..common import standardise_file_name
from yolosegmention.exceptions import FileException


class Getter(BaseGetter):
    _raw_data = None
    _file_names = list()
    _size = list()
    _labels = set()
    _label2id = dict()
    _id2label = dict()
    _label_list = list()
    _id_list = list()

    @property
    def file_name_list(self) -> list[str]:
        """ file_names 无后缀的文件名 """
        return self._file_names

    @property
    def size_list(self) -> list[tuple]:
        """ tuple类型的文件尺寸，形如[(height, width),...] """
        return self._size

    @property
    def labels(self) -> set:
        return self._labels

    @property
    def id2LabelDict(self) -> dict:
        return self._id2label

    @property
    def label2IdDict(self) -> dict:
        return self._label2id

    @property
    def label_list(self) -> list[str]:
        """ 字符串类型的标注图像类别 """
        return self._label_list

    @property
    def id_list(self) -> list[int]:
        """ int类型的标注图像类别 """
        return self._id_list

    def __init__(self, configPath: str):
        """ 解析json文件
        :param configPath: json文件路径
        """
        super().__init__(configPath)
        self.read()
        self.preprocess()

    def read(self) -> None:
        try:
            with open(self.configPath, 'rt') as file:
                self._raw_data = json.load(file)
        except FileNotFoundError or FileExistsError:
            json_path = os.path.abspath(self.configPath)
            raise FileException(f'数据集"{os.path.dirname(json_path)}"缺少名为{os.path.basename(json_path)}的json文件！')
        except json.decoder.JSONDecodeError:
            raise FileException(f'"{os.path.abspath(self.configPath)}"不是一个合法json文件，请核对地址！')

    def preprocess(self) -> None:
        try:
            self._file_names = [file_name for file_name in self._raw_data.keys()]
            tmp_info = [self._raw_data[file_name] for file_name in self._file_names]
            # size is a tuple (height, width)
            self._size = [(info['height'], info['width']) for info in tmp_info]

        except KeyError or AttributeError:
            raise FileException(f'"{os.path.abspath(self.configPath)}"不是一个合法json文件，请核对地址！')
        else:
            for info in tmp_info:
                for bbox_info in info['bbox']:
                    # 添加label到set
                    self._labels.add(bbox_info['label'])
                    # 添加label到list
                    self._label_list.append(bbox_info['label'])
            # 生成 id 标签名称 转换表
            index = 0
            for label in self._labels:
                self._label2id[label] = index
                self._id2label[index] = label
                index += 1

            # 将label list转化为id list
            for label in self._label_list:
                self._id_list.append(self._label2id[label])

    def name2index(self, file_name: str) -> int:
        """
        :param file_name: 文件名，必须为png或jpg格式（是否含后缀均可）
        :return: 返回文件名在json文件中的顺序索引，从0起
        """
        # 若为.png或.jpg结尾的文件名，去除.png或.jpg后缀
        file_name = standardise_file_name(file_name)

        return self._file_names.index(file_name)

    def index2size(self, index: int) -> tuple:
        """
        :param index: 文件在json中的索引，从0起
        :return: 该文件对应图片尺寸
        """
        return self._size[index]

    def name2size(self, file_name: str) -> tuple:
        """
        :param file_name: 文件名，必须为png或jpg格式（是否含后缀均可）
        :return: 文件名对应的图片尺寸
        """
        # 若为.png或.jpg结尾的文件名，去除.png或.jpg后缀
        file_name = standardise_file_name(file_name)

        return self._size[self.name2index(file_name)]

    def label2id(self, label: str) -> int:
        return self._label2id[label]

    def id2label(self, _id: int) -> str:
        return self._id2label[_id]

    def name2id(self, file_name: str) -> int:
        """
        :param file_name: 文件名，必须为png或jpg格式（是否含后缀均可）
        :return: int类型的标注图像类别
        """
        # 若为.png或.jpg结尾的文件名，去除.png或.jpg后缀
        file_name = standardise_file_name(file_name)

        return self._id_list[self.name2index(file_name)]

    def name2label(self, file_name: str) -> int:
        """
        :param file_name: 文件名，必须为png或jpg格式（是否含后缀均可）
        :return: 字符串类型的标注图像类别
        """
        # 若为.png或.jpg结尾的文件名，去除.png或.jpg后缀
        file_name = standardise_file_name(file_name)

        return self._label_list[self.name2index(file_name)]

    def index2label(self, index: int) -> str:
        """
        :param index: 文件名在json文件中的顺序索引，从0起
        :return: 字符串类型的标注图像类别
        """
        return self._label_list[index]

    def index2id(self, index: int) -> int:
        """
        :param index: 文件名在json文件中的顺序索引，从0起
        :return: int类型的标注图像类别
        """
        return self._id_list[index]
