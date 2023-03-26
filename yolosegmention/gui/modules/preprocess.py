"""
@Project ：Graduation-Project-Fluent
@File    ：preprocess.py
@Author  ：X0RB64
@Date    ：2023/03/25 18:01
"""
import os

import qdarkstyle
from qdarkstyle import LightPalette

from ...beans import UNKNOWN_ERR, exit_process
from ...core.dataset.preprocess.create.yolo_v5v8 import Creator
from ...exceptions import FileException, RuntimeException

from ...libs import ToolButton, ComboBox, LineEdit, PrimaryPushButton, ToastToolTip
from ...libs.qfluentwidgets import FluentIcon as Fif

from PyQt6.QtCore import QDir, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (QFileDialog, QProgressBar, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QApplication)


# TODO: 打断处理线程 —— 技术困难：无法安全退出线程     idea: 尝试不打断线程，改为ui界面显示已经打断线程，而等待线程执行结束后清理缓存。
# TODO: 将各种配置转移到设置界面，主界面仅保留执行等按钮

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
                ToastToolTip.warn('警告', str(e), self._parent)
                exit_process(UNKNOWN_ERR)
            index += 1


class PreprocessUI(QWidget):
    _isThreadTerminated = False

    def __init__(self):
        super().__init__()
        self.__create: Creator
        self.__initUI()

    def __initUI(self):
        self.__getComboLabels()
        self.__registerWidgets()

        self.__rootLineEdit.setReadOnly(True)
        self.__srcLineEdit.setReadOnly(True)
        self.__rootLineEdit.setPlaceholderText('默认源数据集父文件夹')
        self.__srcLineEdit.setPlaceholderText('请选择源数据集文件夹')
        self.__destLineEdit.setPlaceholderText('默认为dataset-index')

        # 初始化self.__srcComboBox self.__destComboBox
        self.__srcComboBox.addItems(self.__comboLabels)
        self.__destComboBox.addItems(self.__comboLabels)
        self.__srcComboBox.setCurrentIndex(0)
        self.__destComboBox.setCurrentIndex(1)
        # 按钮绑定槽函数
        self.__srcFileBtn.clicked.connect(self.__srcFileViewSlot)
        self.__processBtn.clicked.connect(self.__processSlot)
        self.__saveBtn.clicked.connect(self.__saveSlot)

        self.__saveBtn.setEnabled(False)
        self.__progressBar.setVisible(False)

        self.__progressBar.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6', palette=LightPalette()))

        # 窗口初始化
        self.setWindowTitle('数据集预处理')
        self.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.__layout)

    def __registerWidgets(self):
        self.__processBtn = PrimaryPushButton('处理')
        self.__saveBtn = PrimaryPushButton('保存')
        self.__progressBar = QProgressBar()
        self.__srcComboBox = ComboBox()
        self.__destComboBox = ComboBox()
        self.__rootLineEdit = LineEdit()
        self.__srcLineEdit = LineEdit()
        self.__destLineEdit = LineEdit()
        self.__srcFileBtn = ToolButton(Fif.FOLDER)
        self.__layout = QHBoxLayout(self)

        qLabels = [
            QLabel('源格式：'),
            QLabel('目标格式:'),
            QLabel('源数据集名：'),
            QLabel('目标数据集名：'),
            QLabel('数据集根目录：')
        ]

        for qLabel in qLabels:
            qLabel.setStyleSheet('''
                QLabel {
                    font: 16px 'Segoe UI', 'Microsoft YaHei';
                }''')

        subVLayouts = [
            QVBoxLayout(),
            QVBoxLayout(),
            QVBoxLayout()
        ]

        subHLayouts = [
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
        ]

        subHLayouts[0].addWidget(self.__srcLineEdit)
        subHLayouts[0].addWidget(self.__srcFileBtn)

        subHLayouts[1].addWidget(self.__destLineEdit)
        subHLayouts[1].insertSpacing(1, 1)

        subHLayouts[2].addWidget(self.__rootLineEdit)

        for label in qLabels:
            subVLayouts[0].addWidget(label)

        subVLayouts[1].addWidget(self.__srcComboBox)
        subVLayouts[1].addWidget(self.__destComboBox)

        subVLayouts[1].addLayout(subHLayouts[0])
        subVLayouts[1].addLayout(subHLayouts[1])
        subVLayouts[1].addLayout(subHLayouts[2])

        subHLayouts[3].addLayout(subVLayouts[0])
        subHLayouts[3].addLayout(subVLayouts[1])

        subVLayouts[2].insertStretch(0)
        subVLayouts[2].addLayout(subHLayouts[3])
        subVLayouts[2].addWidget(self.__progressBar)
        subVLayouts[2].addWidget(self.__processBtn)
        subVLayouts[2].addWidget(self.__saveBtn)
        subVLayouts[2].insertStretch(5)

        self.__layout.insertStretch(0)
        self.__layout.addLayout(subVLayouts[2])
        self.__layout.insertStretch(2)

    def __resetUI(self):
        self.__srcComboBox.setCurrentIndex(0)
        self.__destComboBox.setCurrentIndex(1)
        self.__srcLineEdit.clear()
        self.__destLineEdit.clear()
        self.__rootLineEdit.clear()
        self.__progressBar.setVisible(False)
        self.__saveBtn.setEnabled(False)

    @pyqtSlot()
    def __srcFileViewSlot(self):
        rootPath, rawDatasetFolder = os.path.split(
            QFileDialog.getExistingDirectory(self, '选择源文件夹', QDir.currentPath()))
        self.__srcLineEdit.setText(rawDatasetFolder)
        self.__rootLineEdit.setText(rootPath)

    @pyqtSlot()
    def __processSlot(self):
        # 获取数据
        self.__srcMode = self.__srcComboBox.currentText()
        self.__destMode = self.__destComboBox.currentText()
        self.__rootPath = self.__rootLineEdit.text()
        self.__rawDatasetFolder: str = self.__srcLineEdit.text()
        self.__datasetFolder: str = self.__destLineEdit.text()
        # 核验输入数据是否合法
        if self.__srcMode == '' or self.__destMode == '' or self.__rootPath == '' or self.__rawDatasetFolder == '':
            ToastToolTip.warn('警告', '数据不得为空！', self)
            return
        # 设定默认dataset名
        if self.__datasetFolder == '':
            name = 'dataset'
            if os.path.exists(os.path.join(self.__rootPath, name)):
                index = 1
                while os.path.exists(os.path.join(self.__rootPath, name + str(index))):
                    index += 1
                name += str(index)
            self.__datasetFolder = name
        # 验证self.__srcMode、self.__destMode是否合法
        if not (self.__srcMode in self.__comboLabels and self.__destMode in self.__comboLabels):
            QApplication.exit(UNKNOWN_ERR)
        # TODO: 重构，分离常量数据，使适应各种类型间的数据转换
        # 处理数据
        self.__create = Creator({
            # 根路径
            'ROOT': self.__rootPath,

            # 源数据集信息
            # 源数据文件夹名
            'RAW_DATASET_FOLDER': self.__rawDatasetFolder,
            # 掩膜图片文件夹名
            'MASK_PIC_FOLDER': 'masks',
            # 源图片文件夹名
            'RAW_PIC_FOLDER': 'images',
            # json文件名
            'JSON_NAME': r'kavsir_bboxes.json',
            # 'JSON_NAME': r'bounding-boxes.json',
            # 目标数据集信息
            'DATASET_FOLDER': self.__datasetFolder,
            'YAML_NAME': f'{self.__datasetFolder}.yaml',
        })
        file_names = self.__create.file_names
        self.__progressBar.setTextVisible(True)
        self.__progressBar.setRange(0, len(file_names))
        # ％p — 被完成的百分比取代
        # ％v — 被当前值替换
        # ％m％ — 被总step所取代
        # 默认值是 : ％p％，后一个%为打印字符
        self.__progressBar.setFormat('%v/%m, %p%')
        self.__progressBar.repaint()
        self.__threadObj = Process(self.__create, self)
        self.__threadObj.start()
        self.__threadObj.updateUISignal.connect(self.__processUpdateUISlot)

    @pyqtSlot(int)
    def __processUpdateUISlot(self, value: int):
        self.__progressBar.setVisible(True)
        self.__processBtn.setEnabled(False)
        if not self._isThreadTerminated:
            self.__progressBar.setValue(value)

        if value == self.__progressBar.maximum():
            self.__threadObj.exit()
            ToastToolTip.success('通知', '处理完成，请尽快保存！', self)
            self.__processBtn.setEnabled(True)
            self.__saveBtn.setEnabled(True)
            self.__progressBar.setVisible(False)
            self.__progressBar.setRange(0, 3)

    @pyqtSlot()
    def __saveSlot(self):
        if self.__create is None:
            ToastToolTip.warn('警告', '请先处理数据！', self)
            return
        self.__threadObj = Write(self.__create)
        self.__threadObj.start()
        self.__threadObj.updateUISignal.connect(self.__writeUpdateUISlot)

    @pyqtSlot(int)
    def __writeUpdateUISlot(self, value: int):
        self.__progressBar.setVisible(True)
        self.__progressBar.setValue(value)
        if value == self.__progressBar.maximum():
            del self.__create
            ToastToolTip.success('通知', '写入完成！', self)
            self.__progressBar.setVisible(False)
            self.__saveBtn.setEnabled(False)

    def __getComboLabels(self):
        # TODO: 修改为从数据库中读入
        self.__comboLabels = ['Kvasir-SEG', 'YOLOv8']


def choose_func(src_mode: str, dest_mode: str):
    # TODO: 完成选择函数。负责选定数据集转换格式
    pass
