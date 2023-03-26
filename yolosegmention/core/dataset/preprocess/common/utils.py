"""
@Project ：Graduation-Project-Fluent 
@File    ：utils.py
@Author  ：X0RB64
@Date    ：2023/03/24 15:03 
"""
import os


class NotAcceptableFileTypeException(Exception):
    def __init__(self, path: str):
        tmp = os.path.split(path)
        self._type: str = '.' + tmp[1].split('.')[1]
        if tmp[0] == '':
            self._path = '路径未知！'
        else:
            self._path = f'请检查{tmp[0]}'

    def __str__(self):
        return f"{self._type}为不可接受的文件后缀，请核对后再运行！\n{self._path}"


def standardise_file_name(file_name: str) -> str:
    """
    :param file_name: 文件名，必须为png或jpg格式（是否含后缀均可）
    :return: 不含后缀名的文件名
    """
    if not (file_name.endswith('.png') or file_name.endswith('.jpg')):
        if '.' not in file_name:
            return file_name
        raise NotAcceptableFileTypeException(file_name)
    return file_name[:-4]


def jpg2png(file_path: str) -> str:
    """
    :param file_path: 图片文件路径，含文件后缀
    :return: 修改后的图片文件路径
    """

    if not (file_path.endswith('.jpg') or file_path.endswith('.png')):
        raise NotAcceptableFileTypeException(file_path)

    if file_path.endswith('.jpg'):
        new_path = file_path.replace('.jpg', '.png')
        os.rename(file_path, new_path)
        return new_path
