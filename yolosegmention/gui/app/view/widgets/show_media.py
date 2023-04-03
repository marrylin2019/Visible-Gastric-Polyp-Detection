"""
@Project ：Graduation-Project-Fluent 
@File    ：show_media.py
@Author  ：X0RB64
@Date    ：2023/03/26 15:38 
"""
from PyQt6.QtCore import Qt, pyqtSlot, QUrl, QTime
from PyQt6.QtGui import QResizeEvent, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QLabel, QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ToolButton, HollowHandleStyle, Slider, PrimaryPushButton
from ...common.icon import Icon


class ShowMediaFactory:
    def __init__(self):
        pass

    @staticmethod
    def createColoredLabel(parent: QWidget, text: str = ''):
        return ColoredLabel(parent, text)

    @staticmethod
    def createAutoResizeLabel(parent: QWidget, text: str = ''):
        return AutoResizedImgLabel(parent, text)

    @staticmethod
    def createVideoWidget(parent: QWidget = None):
        return VideoWidget(parent)


class ColoredLabel(QLabel):
    def __init__(self, parent: QWidget, text=''):
        super().__init__(text, parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
        self.setMinimumSize(300, 300)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            'QLabel {background: rgb(211, 211, 211); border: 2px solid rgb(0, 159, 170); border-radius: 10px}')


class AutoResizedImgLabel(ColoredLabel):
    def __init__(self, parent: QWidget, text: str = ''):
        # 必须指定label的父控件，否则本label的size()大小异常！！！
        super().__init__(parent, text)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._processPic(self.pixmap())
        event.accept()
        super().resizeEvent(event)

    def setPixmap(self, pixmap: QPixmap) -> None:
        self._processPic(pixmap)

    def _processPic(self, pixmap: QPixmap):
        pixmap = pixmap
        labelW = self.size().width()
        labelH = self.size().height()

        pixmapW = pixmap.width()
        pixmapH = pixmap.height()

        # 缩放比例为长宽之比中最大的
        pixmap.setDevicePixelRatio(max(pixmapW / labelW, pixmapH / labelH))

        super().setPixmap(pixmap)


class VideoWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._isPlaying = False
        self._srcPlayer = QMediaPlayer(self)
        self._destPlayer = QMediaPlayer(self)
        self._initUI()
        pass

    def _initUI(self):
        self._registerWidgets()

        self._setLabelValue(0, 0)
        self._progressSlider.setStyle(HollowHandleStyle())
        self.setLayout(self._layout)
        self._srcVideoWidget.setMinimumSize(400, 400)
        self._destVideoWidget.setMinimumSize(400, 400)

        self._srcPlayer.setVideoOutput(self._srcVideoWidget)
        self._destPlayer.setVideoOutput(self._destVideoWidget)

        self._bindSlot()

    def _registerWidgets(self):
        # 想想用什么控件承接视频好
        self._srcVideoWidget = QVideoWidget()
        self._destVideoWidget = QVideoWidget()

        self._controlBtn = ToolButton(Icon.PLAY)
        self._progressSlider = Slider(Qt.Orientation.Horizontal, self)
        self._progressInfoLabel = QLabel()

        subHLayout = [
            QHBoxLayout(),
            QHBoxLayout(),
        ]
        self._layout = QVBoxLayout()

        subHLayout[0].addWidget(self._srcVideoWidget)
        subHLayout[0].addWidget(self._destVideoWidget)

        subHLayout[1].addWidget(self._controlBtn)
        subHLayout[1].addWidget(self._progressSlider)
        subHLayout[1].addWidget(self._progressInfoLabel)

        self._layout.addLayout(subHLayout[0])
        self._layout.addLayout(subHLayout[1])

    def _setLabelValue(self, curMs: int, totalMs: int):
        curTime = QTime(0, 0).addMSecs(curMs).toString('mm:ss')
        totalTime = QTime(0, 0).addMSecs(totalMs).toString('mm:ss')
        self._progressInfoLabel.setText(f'{curTime}/{totalTime}')

    def _bindSlot(self):
        self._controlBtn.clicked.connect(self._onControlBtnClicked)
        self._srcPlayer.durationChanged.connect(self._setRange)
        # 进度条跟随，会自动触发slider的valueChanged信号
        self._srcPlayer.positionChanged.connect(lambda t: self._progressSlider.setValue(t))

        self._progressSlider.valueChanged.connect(self._updateProgressInfo)

    def setSource(self, srcVideoPath, destVideoPath):
        self._srcPlayer.setSource(QUrl.fromLocalFile(srcVideoPath))
        self._destPlayer.setSource(QUrl.fromLocalFile(str(destVideoPath)))

    @pyqtSlot()
    def _onControlBtnClicked(self):
        if self._isPlaying:
            self._srcPlayer.pause()
            self._destPlayer.pause()
            self._isPlaying = False
            self._controlBtn.setIcon(Icon.PLAY)
        else:
            self._srcPlayer.play()
            self._destPlayer.play()
            self._isPlaying = True
            self._controlBtn.setIcon(Icon.PAUSE)

    @pyqtSlot()
    def _setRange(self):
        self._progressSlider.setRange(0, self._srcPlayer.duration())

    @pyqtSlot(int)
    def _updateProgressInfo(self, pos: int):
        # 当slider值更新时
        # 更新progressBarInfo
        self._setLabelValue(pos, self._progressSlider.maximum())
        # 将视频跳转到指定位置
        self._srcPlayer.setPosition(pos)
        self._destPlayer.setPosition(pos)
        pass
