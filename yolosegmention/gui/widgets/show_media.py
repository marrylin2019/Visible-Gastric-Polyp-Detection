"""
@Project ：Graduation-Project-Fluent 
@File    ：show_media.py
@Author  ：X0RB64
@Date    ：2023/03/26 15:38 
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent, QPixmap
from PyQt6.QtWidgets import QLabel, QWidget, QSizePolicy

from yolosegmention.beans import COLORS


class ShowMediaFactory:
    def __init__(self):
        pass

    @staticmethod
    def createAutoResizeLabel(parent: QWidget):
        return AutoResizedImgLabel(parent)

    # @staticmethod
    # def createClickedToChooseInput():
    #     return ClickedToChooseInput()


class AutoResizedImgLabel(QLabel):
    def __init__(self, parent: QWidget):
        # 必须指定label的父控件，否则本label的size()大小异常！！！
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setMinimumSize(300, 300)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f'QLabel {{background: rgb{COLORS["LIGHT-GRAY"]}; border: 1;}}')

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__processPic(self.pixmap())
        event.accept()
        super().resizeEvent(event)

    def setPixmap(self, pixmap: QPixmap) -> None:
        self.__processPic(pixmap)

    def __processPic(self, pixmap: QPixmap):
        pixmap = pixmap
        labelW = self.size().width()
        labelH = self.size().height()

        pixmapW = pixmap.width()
        pixmapH = pixmap.height()

        # 缩放比例为长宽之比中最大的
        pixmap.setDevicePixelRatio(max(pixmapW / labelW, pixmapH / labelH))

        super().setPixmap(pixmap)

