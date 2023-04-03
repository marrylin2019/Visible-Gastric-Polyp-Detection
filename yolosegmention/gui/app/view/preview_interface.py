"""
@Project ：Graduation-Project-Fluent 
@File    ：preview_interface.py
@Author  ：X0RB64
@Date    ：2023/03/31 06:29 
"""
import os
from pathlib import Path

import qdarkstyle
from qdarkstyle import LightPalette

from yolosegmention.beans import DatasetTypes
from yolosegmention.core.dataset.preview import generate
from yolosegmention.core.dataset.preprocess.common.check import check

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QDir, Qt, pyqtSlot
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
                             QFileDialog, QListWidgetItem, QInputDialog)
from .widgets import ShowMediaFactory, ListWidget

from ..common.icon import Icon
from qfluentwidgets import (isDarkTheme, ScrollArea, ToolButton, PrimaryPushButton, LineEdit,
                            ComboBox, FluentIcon as Fif, InfoBar, InfoBarIcon)


class PreviewLabelsUI(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__comboLabels: list
        self.__currentPicId: int = -1
        self.__currentPicName: str = ''
        self.__initUI()

    def __initUI(self):
        self.__registerWidgets()

        self.__modeComboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.__listWidget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.__pageNumLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        self.__listWidget.setMinimumHeight(300)
        self.__pageNumLabel.setMaximumHeight(20)
        self.__pageNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__getComboLabels()
        self.__modeComboBox.addItems(self.__comboLabels)
        self.__pathLineEdit.setPlaceholderText('请选择数据集文件夹')

        # 绑定槽函数
        self.__datasetFileBtn.clicked.connect(self.__viewFileSlot)
        self.__processBtn.clicked.connect(self.__processSlot)
        self.__previewBtn.clicked.connect(self.__previewSlot)
        self.__showInExplorerBtn.clicked.connect(self.__showInExplorerSlot)
        self.__listWidget.changePic.connect(self.__changePicSlot)
        self.__listWidget.renamePic.connect(self.__renamePicSlot)
        self.__previousBtn.clicked.connect(self.__previousPicSlot)
        self.__nextBtn.clicked.connect(self.__nextPicSlot)

        self.__previousBtn.setEnabled(False)
        self.__nextBtn.setEnabled(False)
        self.__showInExplorerBtn.setEnabled(False)
        self.__previewBtn.setEnabled(False)

        self.__modeComboBox.setCurrentIndex(0)

        self.__listWidget.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6', palette=LightPalette()))

        self.setLayout(self.__layout)
        self._setQss()

    def __registerWidgets(self):
        self.__pageNumLabel = QLabel()
        qLabels = [
            QLabel('数据集格式：'),
            QLabel('数据集路径：')
        ]
        self.__processBtn = PrimaryPushButton('处理')
        self.__previewBtn = PrimaryPushButton('预览')
        self.__showInExplorerBtn = PrimaryPushButton('在文件资源管理器中显示')

        self.__datasetFileBtn = ToolButton(Fif.FOLDER)

        self.__previousBtn = ToolButton(Icon.PREVIOUS)
        self.__nextBtn = ToolButton(Icon.NEXT)

        self.__pathLineEdit = LineEdit()

        self.__modeComboBox = ComboBox()

        self.__imgLabel = ShowMediaFactory.createAutoResizeLabel(self)

        self.__listWidget = ListWidget()

        self.__layout = QVBoxLayout()
        subVLayouts = [
            QVBoxLayout(),
            QVBoxLayout()
        ]
        subHLayouts = [
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout()
        ]

        subHLayouts[0].addWidget(qLabels[0])
        subHLayouts[0].addWidget(self.__modeComboBox)

        subHLayouts[1].addWidget(qLabels[1])
        subHLayouts[1].addWidget(self.__pathLineEdit)
        subHLayouts[1].addWidget(self.__datasetFileBtn)

        subHLayouts[2].insertStretch(0)
        subHLayouts[2].addWidget(self.__previousBtn)
        subHLayouts[2].addWidget(self.__nextBtn)
        subHLayouts[2].insertStretch(3)

        subVLayouts[0].addWidget(self.__listWidget)
        subVLayouts[0].addWidget(self.__pageNumLabel)

        subVLayouts[1].addWidget(self.__imgLabel)
        subVLayouts[1].addLayout(subHLayouts[2])

        subHLayouts[3].addWidget(self.__showInExplorerBtn)
        subHLayouts[3].addWidget(self.__previewBtn)
        subHLayouts[4].insertSpacing(0, 1)
        subHLayouts[4].addLayout(subVLayouts[0])
        subHLayouts[4].addLayout(subVLayouts[1])

        self.__layout.addSpacing(10)
        self.__layout.addLayout(subHLayouts[0])
        self.__layout.addLayout(subHLayouts[1])
        self.__layout.addWidget(self.__processBtn)
        self.__layout.addLayout(subHLayouts[3])
        self.__layout.addLayout(subHLayouts[4])

    @pyqtSlot()
    def __viewFileSlot(self):
        self.__pathLineEdit.setText(QFileDialog.getExistingDirectory(self, '选择要验证的数据集', QDir.currentPath()))

    @pyqtSlot()
    def __processSlot(self):
        self.__path = ''
        # 获取数据
        mode = ''
        for t in DatasetTypes:
            if t.value == self.__modeComboBox.currentText():
                mode = t
                break
        if mode == '':
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '错误的数据集类型！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        path = self.__pathLineEdit.text()
        # 核验数据
        if not os.path.exists(path):
            if path == '':
                msg = '数据集路径为空！'
            else:
                msg = '数据集路径不存在'
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                msg,
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        configPath = os.path.join(path, [file for file in os.listdir(path) if file.endswith('.yaml')][0])
        checkRes = check(configPath, mode)
        if not checkRes[0]:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                checkRes[1],
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        # TODO: 重构为任意类型可处理
        # 处理数据
        pic_path = os.path.join(path, 'images/train')
        label_path = os.path.join(path, 'labels/train')
        res_path = os.path.join(path, 'labelsVisible')
        num = (lambda n: n if n < 50 else n // 10)(len(os.listdir(pic_path)))
        color_maps = {'0': (98, 9, 11)}

        generate(pic_path, label_path, res_path, num, color_maps)
        self.__path = res_path

        self.__showInExplorerBtn.setEnabled(True)
        self.__previewBtn.setEnabled(True)

    @pyqtSlot()
    def __showInExplorerSlot(self):
        os.startfile(self.__path)

    @pyqtSlot()
    def __previewSlot(self):
        self.__listWidget.clear()

        self.__file_names = []
        for name in os.listdir(self.__path):
            if name.endswith('.png'):
                self.__file_names.append(name)
        # 列表控件添加文件名
        for i in range(len(self.__file_names)):
            item = QListWidgetItem(self.__file_names[i])
            # item.itemChanged.connect(self.__renameVerifySlot)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.__listWidget.insertItem(i, item)
        self.__listWidget.setCurrentItem(self.__listWidget.item(0))
        # 图片控件显示第一张图
        self.__showPicById(0)
        self.__previousBtn.setEnabled(True)
        self.__pageNumLabel.setText(f'{self.__currentPicId + 1}/{len(self.__file_names)}')
        self.__nextBtn.setEnabled(True)
        self.__previewBtn.setEnabled(False)

    def __showPicById(self, file_id: int):
        self.__currentPicId = file_id
        self.__currentPicName = self.__file_names[file_id]
        self.__imgLabel.setPixmap(QPixmap(os.path.join(self.__path, self.__currentPicName)))

    @pyqtSlot()
    def __previousPicSlot(self):
        tmp = (self.__currentPicId - 1) % len(self.__file_names)
        # if tmp not in range(len(self.__file_names)):
        #     return
        self.__currentPicId = tmp
        self.__pageNumLabel.setText(f'{tmp + 1}/{len(self.__file_names)}')
        self.__currentPicName = self.__file_names[tmp]
        self.__listWidget.setCurrentRow(tmp)
        self.__showPicById(tmp)

    @pyqtSlot()
    def __nextPicSlot(self):
        tmp = (self.__currentPicId + 1) % len(self.__file_names)
        # if tmp not in range(len(self.__file_names)):
        #     return
        self.__currentPicId = tmp
        self.__pageNumLabel.setText(f'{tmp + 1}/{len(self.__file_names)}')
        self.__currentPicName = self.__file_names[tmp]
        self.__listWidget.setCurrentRow(tmp)
        self.__showPicById(tmp)

    @pyqtSlot(QListWidgetItem)
    def __changePicSlot(self, item: QListWidgetItem):
        self.__currentPicId = self.__file_names.index(item.text())
        self.__pageNumLabel.setText(f'{self.__currentPicId + 1}/{len(self.__file_names)}')
        self.__currentPicName = self.__file_names[self.__currentPicId]
        self.__showPicById(self.__currentPicId)

    @pyqtSlot(QListWidgetItem)
    def __renamePicSlot(self, item: QListWidgetItem):
        name, ok = QInputDialog.getText(self, "重命名", f'将{item.text()}重命名为：')
        if ok and name:
            if not name.split('.')[-1] == item.text().split('.')[-1]:
                InfoBar(
                    InfoBarIcon.ERROR,
                    '警告',
                    '不允许修改文件名后缀！',
                    Qt.Orientation.Horizontal,
                    isClosable=False,
                    duration=3000,
                    parent=self
                ).show()
                return
            os.rename(os.path.join(self.__path, self.__currentPicName), os.path.join(self.__path, name))
            self.__file_names[self.__file_names.index(self.__currentPicName)] = name
            self.__currentPicName = name

    def __getComboLabels(self):
        self.__comboLabels = [t.value for t in DatasetTypes]

    def _setQss(self):
        """ set style sheet """
        self.setObjectName('scrollWidget')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(str(Path(__file__).parent.parent.joinpath(f'resource/qss/{theme}/setting_interface.qss')),
                  encoding='utf-8') as f:
            self.setStyleSheet(f.read())
