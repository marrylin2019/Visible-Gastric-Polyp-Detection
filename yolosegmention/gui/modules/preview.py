"""
@Project ：GraduationProject 
@File    ：PreviewLabels.py
@Author  ：X0RB64
@Date    ：2023/03/03 17:22

核验新生成的数据集
"""
import os

import qdarkstyle
from qdarkstyle import LightPalette

from yolosegmention.beans import COLORS
from .. import RESOURCES_PATH
from ..widgets import ShowMediaFactory, ListWidget

from Code.Utils.CheckDataset import check
from Code.Scripts.previewImg import generate

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QDir, Qt, pyqtSlot
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel, QSizePolicy,
                             QMessageBox, QFileDialog, QWidget, QListWidgetItem, QInputDialog)


from yolosegmention.libs import ToolButton, FluentIcon as Fif


class PreViewLabelsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.__comboLabels: list
        self.__currentPicId: int = -1
        self.__currentPicName: str = ''
        self.__initUI()

    def __initUI(self):
        self.__registerWidgets()

        self.__previousBtn.setIcon(QIcon(os.path.join(RESOURCES_PATH.absolutePath(), 'previous.png')))
        self.__nextBtn.setIcon(QIcon(os.path.join(RESOURCES_PATH.absolutePath(), 'next.png')))

        self.__modeComboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.__listWidget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.__pageNumLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        self.__listWidget.setMinimumHeight(300)
        self.__pageNumLabel.setMaximumHeight(20)
        self.__pageNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__getComboLabels()
        self.__modeComboBox.addItems(self.__comboLabels)

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

        self.setLayout(self.__layout)
        self.setWindowTitle('标注数据可视化预览')
        self.setWindowIcon(QIcon(os.path.join(RESOURCES_PATH, 'preview_label.png')))

    def __registerWidgets(self):
        self.__pageNumLabel = QLabel()
        qLabels = [
            QLabel('数据集格式：'),
            QLabel('数据集路径：')
        ]
        self.__processBtn = QPushButton('处理')
        self.__previewBtn = QPushButton('预览')
        self.__showInExplorerBtn = QPushButton('在文件资源管理器中显示')

        self.__datasetFileBtn = ToolButton(Fif.FOLDER)

        self.__previousBtn = QPushButton()
        self.__nextBtn = QPushButton()

        self.__pathLineEdit = QLineEdit()

        self.__modeComboBox = QComboBox()

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
        mode = self.__modeComboBox.currentText()
        path = self.__pathLineEdit.text()
        # 核验数据
        if not os.path.exists(path):
            if path == '':
                msg = '数据集路径为空！'
            else:
                msg = '数据集路径不存在'
            QMessageBox.critical(self, '警告', msg)
            return
        checkRes = check(path, mode)
        if not checkRes[0]:
            QMessageBox.critical(self, '警告', checkRes[1])
            return
        # TODO: 重构为任意类型可处理
        # 处理数据
        pic_path = os.path.join(path, 'images/train')
        label_path = os.path.join(path, 'labels/train')
        res_path = os.path.join(path, 'labelsVisible')
        num = (lambda n: n if n < 50 else n // 10)(len(os.listdir(pic_path)))
        # TODO: 颜色设定分离到配置界面
        color_maps = {'0': COLORS['LIGHT-PURPLE']}

        generate(pic_path, label_path, res_path, num, color_maps)
        self.__path = res_path

        self.__showInExplorerBtn.setEnabled(True)
        self.__previewBtn.setEnabled(True)
        self.__processBtn.setEnabled(False)

    @pyqtSlot()
    def __showInExplorerSlot(self):
        os.startfile(self.__path)

    @pyqtSlot()
    def __previewSlot(self):
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
        self.__pageNumLabel.setText(f'{self.__currentPicId+1}/{len(self.__file_names)}')
        self.__nextBtn.setEnabled(True)
        self.__previewBtn.setEnabled(False)

    def __showPicById(self, file_id: int):
        self.__currentPicId = file_id
        self.__currentPicName = self.__file_names[file_id]
        self.__imgLabel.setPixmap(QPixmap(os.path.join(self.__path, self.__currentPicName)))

    @pyqtSlot()
    def __previousPicSlot(self):
        tmp = self.__currentPicId - 1
        if tmp not in range(len(self.__file_names)):
            return
        self.__currentPicId = tmp
        self.__pageNumLabel.setText(f'{tmp+1}/{len(self.__file_names)}')
        self.__currentPicName = self.__file_names[tmp]
        self.__listWidget.setCurrentRow(tmp)
        self.__showPicById(tmp)

    @pyqtSlot()
    def __nextPicSlot(self):
        tmp = self.__currentPicId + 1
        if tmp not in range(len(self.__file_names)):
            return
        self.__currentPicId = tmp
        self.__pageNumLabel.setText(f'{tmp+1}/{len(self.__file_names)}')
        self.__currentPicName = self.__file_names[tmp]
        self.__listWidget.setCurrentRow(tmp)
        self.__showPicById(tmp)

    @pyqtSlot(QListWidgetItem)
    def __changePicSlot(self, item: QListWidgetItem):
        self.__currentPicId = self.__file_names.index(item.text())
        self.__pageNumLabel.setText(f'{self.__currentPicId+1}/{len(self.__file_names)}')
        self.__currentPicName = self.__file_names[self.__currentPicId]
        self.__showPicById(self.__currentPicId)

    @pyqtSlot(QListWidgetItem)
    def __renamePicSlot(self, item: QListWidgetItem):
        name, ok = QInputDialog.getText(self, "重命名", f'将{item.text()}重命名为：')
        if ok and name:
            if not name.split('.')[-1] == item.text().split('.')[-1]:
                QMessageBox.critical(self, '警告', '不允许修改文件名后缀！')
                return
            os.rename(os.path.join(self.__path, self.__currentPicName), os.path.join(self.__path, name))
            self.__file_names[self.__file_names.index(self.__currentPicName)] = name
            self.__currentPicName = name

    def __getComboLabels(self):
        # TODO: 修改为从数据库中读入
        self.__comboLabels = ['YOLOv8', 'Kvasir-SEG']
