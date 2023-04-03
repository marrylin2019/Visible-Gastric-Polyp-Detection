"""
@Project ：Graduation-Project-Fluent 
@File    ：list_widget.py
@Author  ：X0RB64
@Date    ：2023/03/26 15:46 
"""
from PyQt6.QtCore import pyqtSignal, QTimer, pyqtSlot
from PyQt6.QtWidgets import (QListWidget, QListWidgetItem, QApplication)


class ListWidget(QListWidget):
    __isDoubleClicked: bool = False
    __singleClickedItem: QListWidgetItem

    changePic = pyqtSignal(QListWidgetItem)
    renamePic = pyqtSignal(QListWidgetItem)

    def __init__(self):
        super().__init__()
        self.itemClicked.connect(self.__itemClickedSlot)
        self.itemDoubleClicked.connect(self.__itemDoubleClickedSlot)

    @pyqtSlot(QListWidgetItem)
    def __itemClickedSlot(self, item: QListWidgetItem):
        if not self.__isDoubleClicked:
            QTimer.singleShot(QApplication.doubleClickInterval(), self.__itemClickedTimeout)
            self.__singleClickedItem = item

    @pyqtSlot()
    def __itemClickedTimeout(self):
        if not self.__isDoubleClicked:
            # 鼠标单击事件
            self.changePic.emit(self.__singleClickedItem)
        else:
            self.__isDoubleClicked = False

    @pyqtSlot(QListWidgetItem)
    def __itemDoubleClickedSlot(self, item: QListWidgetItem):
        self.__isDoubleClicked = True
        # 鼠标双击击事件
        self.renamePic.emit(item)
