"""
@Project ：Graduation-Project-Fluent 
@File    ：kvasir_seg2yolo_v5v8.py
@Author  ：X0RB64
@Date    ：2023/03/24 15:16 
"""
import os
import cv2
from .base import BaseTranslator
from ..parse.kvasir_seg import Getter
from ..common import standardise_file_name, jpg2png
from yolosegmention.exceptions import FileException, RuntimeException


class Translator(BaseTranslator):
    _isProcessed: dict[str, bool] = dict()

    @property
    def getter(self) -> Getter:
        return self._getter

    @property
    def file_names(self) -> list[str]:
        """Getter获取的文件名"""
        return self.getter.file_name_list

    @property
    def labels(self) -> set:
        return self.getter.labels

    def label2id(self, label: str) -> int:
        return self.getter.label2id(label)

    def __init__(self, configPath: str):
        """
        :param configPath 源数据集json路径
        """
        super().__init__(configPath)
        self._getter = Getter(self.configPath)
        self._results = dict()

    def process(self, maskPicPath: str):
        """
        处理路径为maskPicPath的掩膜图片
        :param maskPicPath: 掩膜图片路径
        """
        if '.' not in maskPicPath:
            raise FileException(f'"{maskPicPath}"缺少文件名后缀，请检查参数！')
        if not maskPicPath.endswith('.png'):
            if not maskPicPath.endswith('.jpg'):
                raise FileException(f'Kvasir-SEG数据集掩膜文件夹"{os.path.abspath(os.path.dirname(maskPicPath))}"中存在非png或jpg格式文件，请核对后再尝试！')
            img_path = jpg2png(maskPicPath)
        else:
            img_path = maskPicPath
        if not os.path.exists(img_path):
            # 文件不存在
            raise FileException(f'掩膜图片"{os.path.abspath(img_path)}"不存在！')
        self._isProcessed[standardise_file_name(os.path.basename(img_path))] = False
        self._get_boundary_data(img_path, self.getter.name2id(os.path.basename(img_path)))

    def _get_boundary_data(self, img_path: str, label_id: int):
        """生成掩膜(mask)边界点集
        :param img_path: 掩模(mask)图片路径
        :param label_id: 该图片的类别id
        """
        try:
            img = cv2.imread(img_path, 0)  # cv2读取图像
            img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]    # 将图片转换为二值图
        except FileNotFoundError or FileExistsError:
            raise FileException(f'"{os.path.abspath(img_path)}"不存在，请检查文件完整性！')
        else:
            boundary_img = cv2.Canny(img, 30, 100)  # cv2边缘处理，得到边缘为255，其余像素为0的图（numpy格式）
            height, width = img.shape
            data = []
            try:
                # 二维数组，先行后列遍历
                for i in range(height):
                    for j in range(width):
                        if boundary_img[i][j] == 255:  # 为255即是边界元素点
                            x_1 = f'{j / width:.6f}'  # 横纵坐标归一化(0 <= x, y <= 1)
                            y_1 = f'{i / height:.6f}'
                            data.append(x_1)
                            data.append(y_1)
            except IndexError:
                raise RuntimeException(f'"{os.path.split(img_path)[1]}" ({", ".join(img.shape)})')
            else:
                self._results[standardise_file_name(os.path.basename(img_path))] = f"{label_id} {' '.join(data)}"
                self._isProcessed[standardise_file_name(os.path.basename(img_path))] = True

    def write_one_to_file(self, pic_name: str, path):
        """ 向指定位置写入
        :param pic_name: 文件名
        :param path: 写入路径
        """
        try:
            with open(path, 'wt') as file:
                if not self._isProcessed[standardise_file_name(pic_name)]:
                    raise RuntimeException(f'"{standardise_file_name(pic_name)}"文件未被处理而写入！')
                file.write(self._results[standardise_file_name(pic_name)])
        except FileNotFoundError or FileExistsError:
            raise FileException(f'"{pic_name}" 未写入，请检查程序！')

    def write_all_to_file(self, base_path, file_names: list[str]):
        """
        :param base_path: 要写入的文件路径，不含文件名
        :param file_names: 要写入的文件名列表
        """
        for file_name in file_names:
            path = os.path.join(base_path, standardise_file_name(file_name)+'.txt')
            self.write_one_to_file(file_name, path)
