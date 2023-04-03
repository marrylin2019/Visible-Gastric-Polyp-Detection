"""
@Project ：Graduation-Project-Fluent 
@File    ：preprocess_interface.py
@Author  ：X0RB64
@Date    ：2023/03/31 02:24 
"""
import os
from ....beans import DatasetTypes
from ....core.dataset.preprocess.create.yolo_v5v8 import Creator
from ....exceptions import FileException, RuntimeException

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import (ScrollArea, ExpandLayout, StateToolTip, SettingCardGroup, ComboBoxSettingCard,
                            PushSettingCard, PrimaryPushSettingCard, isDarkTheme, FluentIcon as Fif, InfoBar, InfoBarIcon)
from ..common.config import cfg
from ..common.icon import Icon


class Write(QThread):
    updateUISignal = pyqtSignal(int)

    def __init__(self, create: Creator):
        super().__init__()
        self._create = create

    def run(self) -> None:
        for i in range(3):
            self._create.write(i)
            self.updateUISignal.emit(i + 1)


class Process(QThread):
    updateUISignal = pyqtSignal(int)

    def __init__(self, create: Creator, parent: QWidget = None):
        super(Process, self).__init__()
        self._create = create
        self._parent = parent

    def run(self):
        file_names = self._create.file_names
        index = 1
        for file_name in file_names:
            try:
                self._create.process(file_name + '.png')
                self.updateUISignal.emit(index)
            except FileException or RuntimeException as e:
                InfoBar(
                    InfoBarIcon.ERROR,
                    '警告',
                    str(e),
                    Qt.Orientation.Horizontal,
                    isClosable=False,
                    duration=3000,
                    parent=self._parent
                ).show()
                return
            index += 1


class TransformInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self._creator = None
        self._rootPath: str = ''
        self._rawDatasetFolder: str = ''
        self._datasetFolder: str = ''
        self._stateToolTip = None

        self._initUI()

        self.srcFolderCard.clicked.connect(self._chooseSrcFolderSlot)
        self.runCard.clicked.connect(self._processSlot)

    def _initUI(self):
        self.formatGroup = SettingCardGroup(
            '格式', self)
        self.srcFormatCard = ComboBoxSettingCard(
            cfg.transformSrcFormat,
            Fif.DOCUMENT,
            '源格式',
            '待转换的数据集格式',
            [t.value for t in DatasetTypes],
            parent=self.formatGroup
        )
        self.destFormatCard = ComboBoxSettingCard(
            cfg.transformDestFormat,
            Fif.DOCUMENT,
            '目标格式',
            '模型需要的数据集格式',
            [t.value for t in DatasetTypes],
            parent=self.formatGroup
        )

        self.folderGroup = SettingCardGroup(
            '文件', self
        )
        self.srcFolderCard = PushSettingCard(
            '选择文件夹',
            Fif.FOLDER,
            '源数据集文件夹',
            cfg.get(cfg.transformSrcFolder),
            self.folderGroup
        )

        self.runGroup = SettingCardGroup(
            '执行', self
        )
        self.runCard = PrimaryPushSettingCard(
            '处理',
            Icon.PREPROCESS,
            '数据转换',
            '请确保输入信息完整',
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
        self.formatGroup.addSettingCard(self.srcFormatCard)
        self.formatGroup.addSettingCard(self.destFormatCard)

        self.folderGroup.addSettingCard(self.srcFolderCard)

        self.runGroup.addSettingCard(self.runCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.formatGroup)
        self.expandLayout.addWidget(self.folderGroup)
        self.expandLayout.addWidget(self.runGroup)

    def _setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(os.path.join(os.path.split(os.path.dirname(__file__))[0], f'resource/qss/{theme}/setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    @pyqtSlot()
    def _chooseSrcFolderSlot(self):
        folder = QFileDialog.getExistingDirectory(
            self, "选择文件夹", cfg.get(cfg.transformSrcFolder))
        if not folder or cfg.get(cfg.transformSrcFolder) == folder:
            return

        cfg.set(cfg.transformSrcFolder, folder)
        self.srcFolderCard.setContent(folder)

    @pyqtSlot()
    def _processSlot(self):
        try:
            self._rootPath, self._rawDatasetFolder = os.path.split(cfg.get(cfg.transformSrcFolder))
        except Exception:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '选择的路径不合法！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        self._srcMode = cfg.get(cfg.transformSrcFormat)
        self._destMode = cfg.get(cfg.transformDestFormat)
        name = 'dataset'
        if os.path.exists(os.path.join(self._rootPath, name)):
            index = 1
            while os.path.exists(os.path.join(self._rootPath, name + str(index))):
                index += 1
            name += str(index)
        self._datasetFolder = name
        try:
            self._creator = Creator({
                # 根路径
                'ROOT': self._rootPath,

                # 源数据集信息
                # 源数据文件夹名
                'RAW_DATASET_FOLDER': self._rawDatasetFolder,
                # 掩膜图片文件夹名
                'MASK_PIC_FOLDER': 'masks',
                # 源图片文件夹名
                'RAW_PIC_FOLDER': 'images',
                # json文件名
                'JSON_NAME': r'kavsir_bboxes.json',
                # 'JSON_NAME': r'bounding-boxes.json',
                # 目标数据集信息
                'DATASET_FOLDER': self._datasetFolder,
                'YAML_NAME': f'{self._datasetFolder}.yaml',
            })
            self._processMax = len(self._creator.file_names)
            self._threadObj = Process(self._creator, self)
            self._stateToolTip = StateToolTip('数据转换', '请耐心等待~', self.window())
            self._stateToolTip.move(self._stateToolTip.getSuitablePos())
            self._stateToolTip.show()
            self._threadObj.start()
            self._threadObj.updateUISignal.connect(self._processUpdateUISlot)
        except FileException or RuntimeException as e:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                str(e),
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
            # ToastToolTip.warn('警告', str(e), self.window())

    @pyqtSlot(int)
    def _processUpdateUISlot(self, value: int):
        if value == self._processMax:
            self._threadObj.quit()
            self._processMax = 3
            self._threadObj = Write(self._creator)
            self._threadObj.start()
            self._threadObj.updateUISignal.connect(self._writeUpdateUISlot)

    @pyqtSlot(int)
    def _writeUpdateUISlot(self, value: int):
        if value == self._processMax:
            # 把生成的数据集文件写入配置文件中
            cfg.set(cfg.transformDestFolder, self._creator.datasetPath)
            del self._creator
            self._stateToolTip.setContent('数据转换完成！')
            self._stateToolTip.setState(True)
            self._threadObj.quit()
