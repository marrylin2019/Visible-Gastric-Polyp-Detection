"""
@Project ：Graduation-Project-Fluent 
@File    ：check.py
@Author  ：X0RB64
@Date    ：2023/03/24 18:08 
"""
import os
import yaml

from yolosegmention.core.dataset.preprocess.parse.kvasir_seg import Getter
from yolosegmention.beans import DatasetTypes


def check(configPath: str, datasetType: DatasetTypes) -> tuple[bool, str]:
    """
    :param configPath: 配置文件路径
    :param datasetType: 模型类型
    :return:
    """
    if not os.path.exists(configPath):
        return False, '源数据集文件路径不存在！'
    return dataset_check_funcs[datasetType](configPath)


def check_Kvasir_SEG(path: str) -> tuple[bool, str]:
    path = os.path.dirname(path)
    result = (False, '提供的原始数据集非Kvasir-SEG数据集或该数据集不完整')
    sub_files = ['images', 'masks', 'kavsir_bboxes.json']
    # sub_files = ['images', 'masks', 'bounding-boxes.json']
    for sub_file in sub_files:
        if not os.path.exists(os.path.join(path, sub_file)):
            return result
    for file_name in Getter(os.path.join(path, sub_files[2])).file_name_list:
        if not ((os.path.exists(os.path.join(path, sub_files[0], file_name + '.png')) or os.path.exists(os.path.join(path, sub_files[0], file_name + '.jpg'))) and
                (os.path.exists(os.path.join(path, sub_files[1], file_name + '.png')) or os.path.exists(os.path.join(path, sub_files[1], file_name + '.jpg')))):
            return result
    return True, ''


def check_YOLOv5v8(path: str) -> tuple[bool, str]:
    configFileName = os.path.basename(path)
    configFilePath = path
    # 核验是否存在dataset_file_name.yaml
    if not os.path.exists(configFilePath):
        return False, f'请检查"{os.path.normpath(path)}"下是否存在yaml文件，若存在，请确保该文件名为"{configFileName}"'

    result = (False, '提供的原始数据集非YOLOv8数据集或该数据集不完整')
    # 核验yaml是否完整
    with open(configFilePath, 'rt') as file:
        fileInfo = yaml.load(file.read(), yaml.FullLoader)
    yamlKeys = ['test', 'train', 'val', 'names', 'path']
    for key in yamlKeys:
        if key not in fileInfo.keys():
            return result

    if fileInfo['train'] == '':
        return result

    imgFolderName = 'images'
    labelFolderName = 'labels'

    # 核验训练集、测试集和验证集中，标签文件名与图片对应
    for key in yamlKeys[:3]:
        if not fileInfo[key] == '':
            if not set([name.split('.')[0] for name in os.listdir(os.path.join(fileInfo['path'], imgFolderName, key))]) ==\
                   set([name.split('.')[0] for name in os.listdir(os.path.join(fileInfo['path'], labelFolderName, key))]):
                return result
    return True, ''


def check_YOLOv7(path: str) -> tuple[bool, str]:
    # TODO: 完成YOLOv7的检查
    return True, ''


def check_UNETPP(path: str) -> tuple[bool, str]:
    # TODO: 完成UNETPP的检查
    return True, ''


dataset_check_funcs = {
    DatasetTypes.KVASIR_SEG: check_Kvasir_SEG,
    DatasetTypes.YOLOv5: check_YOLOv5v8,
    DatasetTypes.YOLOv7: check_YOLOv7,
    DatasetTypes.YOLOv8: check_YOLOv5v8,
    DatasetTypes.UNETPP: check_UNETPP,
}
