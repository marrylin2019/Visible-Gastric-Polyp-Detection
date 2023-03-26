"""
@Project ：Graduation-Project-Fluent 
@File    ：yolo_v5v8.py
@Author  ：X0RB64
@Date    ：2023/03/24 16:28 
"""
import os
import yaml
import shutil

from .base import BaseCreator
from ..common import jpg2png, Slicer
from ..translate.kvasir_seg2yolo_v5v8 import Translator
from yolosegmention.exceptions import FileException, RuntimeException


class Creator(BaseCreator):
    @property
    def translator(self) -> Translator:
        return self._translator

    @property
    def file_names(self) -> list[str]:
        """ 无后缀的文件名列表 """
        return self._names

    @property
    def datasetPath(self) -> str:
        return self._DATA['DATASET_PATH']

    def __init__(self, data: dict):
        self._isProcessed = False
        self._names: list[str]
        self._slice: Slicer
        self._TARGET_TAGS = [
            [
                'images',
                'labels',
            ],
            [
                'train',
                'val',
            ]
        ]

        # TODO: 改为从配置文件中读取数据
        # 初始化_PATH
        self._DATA = data
        self._DATA['RAW_DATASET_PATH'] = os.path.join(self._DATA['ROOT'], self._DATA['RAW_DATASET_FOLDER'])
        self._DATA.pop('RAW_DATASET_FOLDER')
        self._DATA['MASK_PIC_PATH'] = os.path.join(self._DATA['RAW_DATASET_PATH'], self._DATA['MASK_PIC_FOLDER'])
        self._DATA.pop('MASK_PIC_FOLDER')
        self._DATA['RAW_PIC_PATH'] = os.path.join(self._DATA['RAW_DATASET_PATH'], self._DATA['RAW_PIC_FOLDER'])
        self._DATA.pop('RAW_PIC_FOLDER')
        self._DATA['DATASET_PATH'] = os.path.join(self._DATA['ROOT'], self._DATA['DATASET_FOLDER'])
        self._DATA.pop('DATASET_FOLDER')
        self._DATA['JSON_PATH'] = os.path.join(self._DATA['RAW_DATASET_PATH'], self._DATA['JSON_NAME'])
        self._DATA.pop('JSON_NAME')
        self._DATA['YAML_PATH'] = os.path.join(self._DATA['DATASET_PATH'], self._DATA['YAML_NAME'])
        self._DATA.pop('YAML_NAME')
        self._DATA[self._TARGET_TAGS[0][0]] = dict()
        self._DATA[self._TARGET_TAGS[0][1]] = dict()

        super().__init__(self._DATA['JSON_PATH'])
        # 必须在调用父类构造函数后实例化Translator
        self._translator = Translator(self.configPath)

        self._check_exists()
        self._create_structure()
        self._jpg2png()
        self._names = self.translator.file_names
        self._slicer = Slicer(self._names)

    def _check_exists(self):
        if os.path.exists(self._DATA['DATASET_PATH']):
            raise FileException(f"数据集已存在，请检查数据集是否完整后再运行！\n数据集路径：{os.path.abspath(self._DATA['DATASET_PATH'])}")

    def _create_structure(self):
        for lv0_tag in self._TARGET_TAGS[0]:
            if os.path.exists(os.path.join(self._DATA['DATASET_PATH'], lv0_tag)):
                raise FileException(f"数据集已存在，请检查数据集是否完整后再运行！\n数据集路径：{os.path.abspath(self._DATA['DATASET_PATH'])}")
            for lv1_tag in self._TARGET_TAGS[1]:
                path = os.path.join(self._DATA['DATASET_PATH'], lv0_tag, lv1_tag)
                self._DATA[lv0_tag][lv1_tag] = path
                os.makedirs(path)

    def _jpg2png(self):
        """
        将源数据集中jpg转化为png
        :return:
        """
        try:
            mask_pic_paths = [os.path.join(self._DATA['MASK_PIC_PATH'], name) for name in os.listdir(self._DATA['MASK_PIC_PATH'])]
            raw_pic_paths = [os.path.join(self._DATA['RAW_PIC_PATH'], name) for name in os.listdir(self._DATA['RAW_PIC_PATH'])]
            files_paths = mask_pic_paths + raw_pic_paths
            for files_path in files_paths:
                jpg2png(files_path)
        except FileNotFoundError as e:
            raise FileException(f'数据集{e.filename}不存在！')

    def _write_imgs(self):
        for name in self._slicer.train_set:
            shutil.copy(os.path.join(self._DATA['RAW_PIC_PATH'], name + '.png'),
                        os.path.join(self._DATA[self._TARGET_TAGS[0][0]][self._TARGET_TAGS[1][0]], name + '.png'))
        for name in self._slicer.val_set:
            shutil.copy(os.path.join(self._DATA['RAW_PIC_PATH'], name + '.png'),
                        os.path.join(self._DATA[self._TARGET_TAGS[0][0]][self._TARGET_TAGS[1][1]], name + '.png'))

    def _write_labels(self):
        self.translator.write_all_to_file(self._DATA[self._TARGET_TAGS[0][1]][self._TARGET_TAGS[1][0]], self._slicer.train_set)
        self.translator.write_all_to_file(self._DATA[self._TARGET_TAGS[0][1]][self._TARGET_TAGS[1][1]], self._slicer.val_set)

    def _write_yaml(self):
        table = dict()
        for label in self.translator.labels:
            table[self.translator.label2id(label)] = label
        with open(self._DATA['YAML_PATH'], 'wt') as file:
            yaml.dump({
                'names': table,
                'path': os.path.normpath(self._DATA['DATASET_PATH']),  # dataset root dir (leave empty for HUB)
                'train': 'images/train',  # train images (relative to 'path') 8 images
                'val': 'images/val',  # val images (relative to 'path') 8 images
                'test': '',  # test images (optional)
            }, file)

    def process(self, file_name: str) -> None:
        """
        :param file_name: 带后缀的文件名
        """
        self._isProcessed = True
        self.translator.process(os.path.join(self._DATA['MASK_PIC_PATH'], file_name))

    def write(self, num: int) -> None:
        """
        :param num: 写入种类 [0: write_imgs, 1: write_labels, 2: write_yaml]
        :return:
        """
        if self._isProcessed:
            [self._write_imgs, self._write_labels, self._write_yaml][num]()
        else:
            raise RuntimeException(f'非法的操作顺序：图片未经处理而写入！')
