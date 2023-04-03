"""
@Project ：Graduation-Project-Fluent 
@File    ：predict_interface.py
@Author  ：X0RB64
@Date    ：2023/04/03 11:53 
"""
import os
import re
import shutil
from enum import Enum
from pathlib import Path

import qdarkstyle
from qdarkstyle import LightPalette


from yolosegmention.beans import COLORS, DatasetTypes, StreamTypes, PATTERNS
from yolosegmention.core.dataset.preview import generate
from yolosegmention.core.dataset.preprocess.common.check import check

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QDir, Qt, pyqtSlot, QThread, pyqtSignal
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
                             QFileDialog, QListWidgetItem, QInputDialog, QWidget)

from yolosegmention.core.models.yolov8.predict import predict
from yolosegmention.exceptions import RuntimeException
from .widgets import ShowMediaFactory, ListWidget
from .widgets.show_media import VideoWidget

from ..common.icon import Icon
from qfluentwidgets import (isDarkTheme, ScrollArea, ToolButton, PrimaryPushButton, LineEdit,
                            ComboBox, FluentIcon as Fif, InfoBar, InfoBarIcon, StateToolTip, MessageBox)


class Predict(QThread):
    finished = pyqtSignal()

    def __init__(self, _type: str, path: str, preWeightsPath: str, parent: QWidget):
        super().__init__()
        self._type = _type
        self._path = path
        self.__preWeightsPath = preWeightsPath
        self._parent = parent

    def run(self) -> None:
        try:
            predict(self._type, self._path, self.__preWeightsPath)
            self.finished.emit()
        except RuntimeException as e:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                str(e),
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self._parent
            ).show()
            self.finished.disconnect()
        pass


class PredictInterface(ScrollArea):
    def __init__(self, root: Path, parent=None):
        super().__init__(parent)
        self._root = root
        self.SHOULD_SKIP_RM_CACHE = False
        self.resize(1000, 800)
        self._initUI()
        self.setLayout(self._layout)

    def _initUI(self):
        self._regWidget()
        self._bindSlot()

        self._streamTypeComboBox.addItems([item.value for item in StreamTypes])
        self._streamTypeComboBox.setCurrentIndex(0)

        self._streamTypeComboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self._layout.setContentsMargins(20, 20, 20, 20)

        self._setQss()
        pass

    def _regWidget(self):
        self._layout = QVBoxLayout(self)
        self._labelParent = QHBoxLayout(self)
        subHLayout = [
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
        ]
        self._labelParent = subHLayout[2]

        qLabel = [
            QLabel('输入流类型:\t'),
            QLabel('请选择路径:\t'),
        ]

        self._streamTypeComboBox = ComboBox()
        self._pathLineEdit = LineEdit()
        self._fileBtn = ToolButton(Fif.FOLDER)
        self._srcLabel = ShowMediaFactory.createColoredLabel(self, '输入')
        self._destLabel = ShowMediaFactory.createColoredLabel(self, '输出')
        self._startBtn = PrimaryPushButton('开始预测')
        self._videoWidget = ShowMediaFactory.createVideoWidget()

        subHLayout[0].addWidget(qLabel[0])
        subHLayout[0].addWidget(self._streamTypeComboBox)

        subHLayout[1].addWidget(qLabel[1])
        subHLayout[1].addWidget(self._pathLineEdit)
        subHLayout[1].addWidget(self._fileBtn)

        subHLayout[2].addWidget(self._srcLabel)
        subHLayout[2].addWidget(self._destLabel)

        self._layout.addLayout(subHLayout[0])
        self._layout.addLayout(subHLayout[1])
        self._layout.addWidget(self._startBtn)
        self._layout.addLayout(self._labelParent)

    def _bindSlot(self):
        self._fileBtn.clicked.connect(self._onFileBtnClicked)
        self._streamTypeComboBox.currentTextChanged.connect(self.__currentTextChangedSlot)
        self._startBtn.clicked.connect(self._onStartBtnClicked)

    def _changeSrcDestLabels(self, srcWidget: QWidget, destWidget: QWidget):
        self._labelParent.removeWidget(self._srcLabel)
        self._labelParent.removeWidget(self._destLabel)

        self._srcLabel.destroy()
        self._destLabel.destroy()

        self._srcLabel = srcWidget
        self._destLabel = destWidget

        self._labelParent.addWidget(self._srcLabel)
        self._labelParent.addWidget(self._destLabel)

    @pyqtSlot()
    def _onFileBtnClicked(self):
        try:
            curType = StreamTypes(self._streamTypeComboBox.currentText())
        except ValueError:
            # 报错
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '错误的数据类型！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        else:
            _filter = {
                StreamTypes.PICTURE: '图片文件(*.jpg *.png *.bmp *.dng *.jpeg *.mpo *.tif *.tiff *.webp *.pfm)',
                StreamTypes.VIDEO: '视频文件(*.asf *.avi *.gif *.m4v *.mkv *.mov *.mp4 *.mpeg *.mpg *.ts *.wmv *.webm)'
            }[curType]
            path = QFileDialog.getOpenFileName(self, f'请选择{curType.value}路径', QDir.currentPath(), _filter)
            self._pathLineEdit.setText(path[0])

    @pyqtSlot(str)
    def __currentTextChangedSlot(self, curTxt: str):
        try:
            curTxt = StreamTypes(curTxt)
        except ValueError:
            # 报错
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '错误的数据类型！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        else:
            text = ''
            visible = True
            if curTxt == StreamTypes.PICTURE:
                placeholderText = '输入图片路径'
            elif curTxt == StreamTypes.VIDEO:
                placeholderText = '输入视频路径'
            elif curTxt == StreamTypes.STREAM:
                placeholderText = '必须为rtmp://'
                text = 'rtmp://'
                visible = False
            else:
                raise RuntimeException('Unreachable code!')
            self._pathLineEdit.setPlaceholderText(placeholderText)
            self._pathLineEdit.setText(text)
            self._fileBtn.setVisible(visible)

    @pyqtSlot()
    def _onStartBtnClicked(self):
        self._type = self._streamTypeComboBox.currentText()
        self._path = self._pathLineEdit.text()
        if self._path == '':
            InfoBar(
                InfoBarIcon.WARNING,
                '提示',
                '路径信息不得为空！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        self._threadObj = Predict(self._type, self._path, str(Path(__file__).parent.parent.joinpath('resource/pre-weights/best.pt')), self)
        self._startBtn.setEnabled(False)
        self._stateToolTip = StateToolTip('预测数据', '请耐心等待~', self.window())
        self._stateToolTip.move(self._stateToolTip.getSuitablePos())
        self._stateToolTip.show()
        self._threadObj.finished.connect(self._predictFinishedSlot)
        self._threadObj.start()

    @pyqtSlot()
    def _predictFinishedSlot(self):
        t = StreamTypes(self._type)
        predictFolder = self._root.joinpath('runs/segment/')
        if not predictFolder.exists():
            self._stateToolTip.setContent('预测失败，捕获到一个异常信息！')
            self._stateToolTip.setState(True)
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '程序异常：未产生预测文件，请联系管理员修复！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        predictFolder = predictFolder.joinpath(
            max([folder if re.match('predict\d{0,3}', folder) else '' for folder in os.listdir(predictFolder)]))
        if t == StreamTypes.PICTURE:
            # 图片
            picList = []
            for filename in os.listdir(predictFolder):
                if re.match('.*?\\.(jpg|png|bmp|dng|jpeg|mpo|tif|tiff|webp|pfm)', filename) is not None:
                    picList.append(filename)
            picPath = predictFolder.joinpath(picList[0])
            self._changeSrcDestLabels(ShowMediaFactory.createAutoResizeLabel(self),
                                      ShowMediaFactory.createAutoResizeLabel(self))
            self._srcLabel.setPixmap(QPixmap(self._path))
            self._destLabel.setPixmap(QPixmap(str(picPath)))
        elif t == StreamTypes.VIDEO:
            # 视频
            videoList = []
            for filename in os.listdir(predictFolder):
                if re.match('.*?\\.(asf|avi|gif|m4v|mkv|mov|mp4|mpeg|mpg|ts|wmv|webm)', filename) is not None:
                    videoList.append(filename)
            destVideoPath = predictFolder.joinpath(videoList[0])
            self._destLabel.setParent(None)
            self._srcLabel.setParent(None)
            self._srcLabel.destroy()
            self._destLabel.destroy()
            self._labelParent.addWidget(self._videoWidget)
            self.repaint()
            self._videoWidget.setSource(self._path, destVideoPath)
            pass
        elif t == StreamTypes.STREAM:
            # 视频流
            pass
        else:
            raise RuntimeException('Unreachable code!')

        self._startBtn.setEnabled(True)
        if not predictFolder.exists():
            self._stateToolTip.setContent('预测失败，捕获到一个异常信息！')
            self._stateToolTip.setState(True)
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '程序异常：未产生预测文件，请联系管理员修复！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        self._stateToolTip.setContent('预测成功！')
        self._stateToolTip.setState(True)
        if self.SHOULD_SKIP_RM_CACHE or not t == StreamTypes.PICTURE:
            return
        try:
            shutil.rmtree(str(predictFolder))
        except PermissionError or OSError:
            msg = MessageBox('警告',
                             f'无法删除缓存文件{str(predictFolder)}\n是否不再尝试自动清理缓存文件？\n（'
                             f'可在程序运行结束后删除{str(predictFolder.parent)}中的predict文件夹）',
                             self)
            msg.yesSignal.connect(self._ignoreRemoveCacheSlot)
            msg.show()

    @pyqtSlot()
    def _ignoreRemoveCacheSlot(self):
        self.SHOULD_SKIP_RM_CACHE = True

    def _setQss(self):
        """ set style sheet """
        self.setObjectName('scrollWidget')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(str(Path(__file__).parent.parent.joinpath(f'resource/qss/{theme}/setting_interface.qss')),
                  encoding='utf-8') as f:
            self.setStyleSheet(f.read())
