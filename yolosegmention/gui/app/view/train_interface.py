"""
@Project ：Graduation-Project-Fluent
@File    ：train_interface.py
@Author  ：X0RB64
@Date    ：2023/03/31 06:57
"""
import os
from yolosegmention.core.models.yolov8.train import train
from yolosegmention.beans.dataset_model_types import ModelTypes
from PyQt6.QtCore import pyqtSlot, QThread, Qt, pyqtSignal
from PyQt6.QtWidgets import (QFileDialog, QWidget)

from yolosegmention.exceptions import RuntimeException
from ..common.config import cfg
from ..common.icon import Icon
from qfluentwidgets import (StateToolTip, isDarkTheme, ScrollArea, ExpandLayout, SettingCardGroup,
                            PrimaryPushSettingCard, RangeSettingCard, PushSettingCard, ComboBoxSettingCard, ConfigItem,
                            SettingCard, InfoBarPosition, InfoBar, InfoBarIcon, FluentIcon as Fif, )


class TrainModel(QThread):
    exceptionSignal = pyqtSignal(Exception)

    def __init__(self, mode: ModelTypes, datasetPath: str, preWeightPath: str, batch: int, epochs: int):
        super().__init__()
        # 获取modelType, datasetPath, preWeightPath, epochs和batch

        self.mode = mode
        self.datasetPath = datasetPath
        self.preWeightPath = preWeightPath
        self.batch = batch
        self.epochs = epochs

    def run(self):
        try:
            # 根据选择的不同模型执行不同函数
            if self.mode == ModelTypes.YOLOv8_SEGMENT:
                train(self.preWeightPath, self.datasetPath, epochs=self.epochs, batch=self.batch)
            elif self.mode == ModelTypes.YOLOv8_DETECTION:
                raise RuntimeException('未实现的模型')
            elif self.mode == ModelTypes.YOLOv7_DETECTION:
                raise RuntimeException('未实现的模型')
            elif self.mode == ModelTypes.YOLOv5_DETECTION:
                raise RuntimeException('未实现的模型')
            elif self.mode == ModelTypes.UNETPP:
                raise RuntimeException('未实现的模型')
            else:
                raise RuntimeException('Unreachable Code!')
        except Exception as e:
            self.finished.disconnect()
            self.exceptionSignal.emit(e)
            self.quit()


class TrainUI(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self._stateToolTip = None
        self.__initUI()

        self.datasetPathCard.clicked.connect(lambda: self._fileBtnSlot("选择数据集配置文件", 'Dataset Config File (*.yaml)', cfg.trainDatasetFolder, self.datasetPathCard))
        self.preWeightPathCard.clicked.connect((lambda: self._fileBtnSlot("选择预训练权重文件", 'Pre-Weight File (*.pt *.yaml)', cfg.trainPreWeightFolder, self.preWeightPathCard)))
        self.runCard.clicked.connect(self.__trainSlot)

    def __initUI(self):
        self.configGroup = SettingCardGroup(
            '配置', self
        )
        self.modelCard = ComboBoxSettingCard(
            cfg.trainModelFormat,
            Fif.DOCUMENT,
            '选择模型',
            '选择要训练的模型种类',
            [t.value for t in ModelTypes],
            parent=self.configGroup
        )
        self.datasetPathCard = PushSettingCard(
            '选择文件夹',
            Fif.FOLDER,
            '数据集文件夹',
            cfg.get(cfg.trainDatasetFolder),
            self.configGroup
        )
        self.preWeightPathCard = PushSettingCard(
            '选择文件夹',
            Fif.FOLDER,
            '预训练权重文件',
            cfg.get(cfg.trainPreWeightFolder),
            self.configGroup
        )
        self.batchCard = ComboBoxSettingCard(
            cfg.trainBatch,
            Icon.BATCH,
            '选择batch',
            '同时训练的图片数量',
            texts=['8', '16', '32'],
            parent=self.configGroup
        )
        self.epochsCard = RangeSettingCard(
            cfg.trainEpochs,
            Icon.EPOCH,
            '训练轮次',
            parent=self.configGroup
        )

        self.runGroup = SettingCardGroup(
            '执行', self
        )
        self.runCard = PrimaryPushSettingCard(
            '开始训练',
            Icon.TRAIN_MODEL,
            '模型训练',
            '请保证输入信息完整',
            self.runGroup
        )
        self._initWidget()

    def _initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        # initialize style sheet
        self._setQss()

        # initialize layout
        self._initLayout()

    def _initLayout(self):
        # add cards to group
        self.configGroup.addSettingCard(self.modelCard)
        self.configGroup.addSettingCard(self.datasetPathCard)
        self.configGroup.addSettingCard(self.preWeightPathCard)
        self.configGroup.addSettingCard(self.batchCard)
        self.configGroup.addSettingCard(self.epochsCard)
        self.runGroup.addSettingCard(self.runCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.configGroup)
        self.expandLayout.addWidget(self.runGroup)

    def _fileBtnSlot(self, title: str, fileFilter: str, configItem: ConfigItem, card: SettingCard):
        file = QFileDialog.getOpenFileName(self, title, os.path.dirname(cfg.get(configItem)), fileFilter)[0]
        if not file or cfg.get(configItem) == file:
            return
        cfg.set(configItem, file)
        card.setContent(file)

    @pyqtSlot()
    def __trainSlot(self):
        # 获取数据
        mode = ''
        for t in ModelTypes:
            if t == cfg.get(cfg.trainModelFormat):
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
        datasetPath = cfg.get(cfg.trainDatasetFolder)
        preWeightPath = cfg.get(cfg.trainPreWeightFolder)
        # 核验数据
        if not (os.path.exists(datasetPath) and os.path.exists(preWeightPath)):
            if datasetPath == '' or preWeightPath == '':
                msg = '数据集或预训练权重文件路径为空！'
            else:
                msg = '数据集或预训练权重文件路径不存在'
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

        batch = cfg.get(cfg.trainBatch)
        epochs = cfg.get(cfg.trainEpochs)
        # UI处理
        self.runCard.setEnabled(False)
        # TODO: 重构为任意模型可训练
        # 训练
        self.__threadObj = TrainModel(mode, datasetPath, preWeightPath, batch, epochs)
        self._stateToolTip = StateToolTip('训练模型', '请耐心等待~', self.window())
        self._stateToolTip.move(self._stateToolTip.getSuitablePos())
        self._stateToolTip.show()
        self.__threadObj.start()
        self.__threadObj.exceptionSignal.connect(self._trainExceptionSlot)
        self.__threadObj.finished.connect(self.__finishedTrainSlot)

    @pyqtSlot(Exception)
    def _trainExceptionSlot(self, e: Exception):
        self._stateToolTip.setContent('训练失败，捕获到一个错误信息')
        InfoBar.error(
            title='异常信息',
            content=str(e),
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )
        self._stateToolTip.setState(True)
        self.runCard.setEnabled(True)

    @pyqtSlot()
    def __finishedTrainSlot(self):
        self._stateToolTip.setContent('模型训练完成！')
        self._stateToolTip.setState(True)
        self.runCard.setEnabled(True)

    def _setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(os.path.join(os.path.split(os.path.dirname(__file__))[0],
                               f'resource/qss/{theme}/setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
