# coding:utf-8
import os.path
from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from qfluentwidgets import (ScrollArea, SettingCardGroup, isDarkTheme)
from ..common.config import cfg


class PageTitleBar(QWidget):
    """ Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.subtitleLabel = QLabel(subtitle, self)
        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(138)
        self.titleLabel.setObjectName('titleLabel')
        self.subtitleLabel.setObjectName('subtitleLabel')


class BaseInterface(ScrollArea):
    """ base interface """

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        subtitle: str
            The subtitle of gallery

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = PageTitleBar(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)

    # def addCardGroup(self, group: SettingCardGroup):
    #     self.vBoxLayout.addWidget(group, 0, Qt.AlignmentFlag.AlignTop)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())

    def __setQss(self):
        self.view.setObjectName('view')
        theme = 'dark' if isDarkTheme() else 'light'
        with open(os.path.join(os.path.split(os.path.dirname(__file__))[0], f'resource/qss/{theme}/gallery_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
