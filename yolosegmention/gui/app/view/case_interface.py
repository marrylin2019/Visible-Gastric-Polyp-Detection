"""
@Project ：Graduation-Project-Fluent 
@File    ：case_interface.py
@Author  ：X0RB64
@Date    ：2023/04/02 15:39 
"""
import datetime
import time
import uuid
from pathlib import Path

import qdarkstyle
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from qdarkstyle import LightPalette
from qfluentwidgets import ScrollArea, LineEdit, ComboBox, ToolButton, FluentIcon as Fif, PrimaryPushButton, SpinBox, \
    InfoBar, InfoBarIcon, MessageBox

from yolosegmention.exceptions import SqlNoMatchException, SqlCannotConnectException, SqlException, RuntimeException
from yolosegmention.gui.app.common.mysql import Mysql
from yolosegmention.libs.qfluentwidgets import isDarkTheme


class CaseInterface(ScrollArea):
    def __init__(self, nickname: str, _uuid: str, parent=None):
        super().__init__(parent)
        self.nickname = nickname
        self._uuid = _uuid
        self._mysql = Mysql()
        self._isEditing = False
        self._isSearched = False
        self.resize(1000, 800)
        self._initUI()
        self.setLayout(self._layout)

    def _initUI(self):
        self._registerWidget()
        self._ageSpinBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self._genderComboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self._genderComboBox.addItems(['男', '女'])
        self._genderComboBox.setCurrentIndex(0)
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._ageSpinBox.setValue(0)

        self._widgetInit()
        self._oldCaseTextEdit.setReadOnly(True)
        self._idLineEdit.setText('d286de4e-3b1c-457c-9259-e3b599c92433')
        # self._widgetOpen()

        self.setObjectName('scrollWidget')
        self._oldCaseTextEdit.setObjectName('oldCaseTextEdit')
        self._diagnoseTextEdit.setObjectName('diagnoseTextEdit')

        self._bindSlot()
        self._setQss()

    def _registerWidget(self):
        self._layout = QVBoxLayout()
        subVLayout = [
            QVBoxLayout(),
            QVBoxLayout(),
        ]
        subHLayout = [
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
            QHBoxLayout(),
        ]
        qLabels = [
            QLabel('序号:\t'),
            QLabel('姓名:\t'),
            QLabel('年龄:\t'),
            QLabel('性别:\t'),
            QLabel('既往病史:'),
            QLabel('诊断结果:'),
        ]

        self._idLineEdit = LineEdit()
        self._searchBtn = ToolButton(Fif.SEARCH)
        self._nameLineEdit = LineEdit()
        self._ageSpinBox = SpinBox()
        self._genderComboBox = ComboBox()
        self._oldCaseTextEdit = QTextEdit()
        self._diagnoseTextEdit = QTextEdit()
        self._submitBtn = PrimaryPushButton('提交')
        self._addNewCaseBtn = PrimaryPushButton('新建病历')

        subHLayout[0].addWidget(qLabels[0])
        subHLayout[0].addWidget(self._idLineEdit)
        subHLayout[0].addWidget(self._searchBtn)

        subHLayout[1].addWidget(qLabels[1])
        subHLayout[1].addWidget(self._nameLineEdit)

        subHLayout[2].addWidget(qLabels[2])
        subHLayout[2].addWidget(self._ageSpinBox)

        subHLayout[3].addWidget(qLabels[3])
        subHLayout[3].addWidget(self._genderComboBox)

        subVLayout[0].addWidget(qLabels[4])
        subVLayout[0].insertStretch(1)
        subHLayout[4].addLayout(subVLayout[0])
        subHLayout[4].addWidget(self._oldCaseTextEdit)

        subVLayout[1].addWidget(qLabels[5])
        subVLayout[1].insertStretch(1)
        subHLayout[5].addLayout(subVLayout[1])
        subHLayout[5].addWidget(self._diagnoseTextEdit)

        for hLayout in subHLayout:
            self._layout.addLayout(hLayout)

        self._layout.addWidget(self._addNewCaseBtn)
        self._layout.addWidget(self._submitBtn)

    def _widgetInit(self):
        self._widgetClose()
        self._idLineEdit.setEnabled(True)
        self._searchBtn.setEnabled(True)
        # self._addNewCaseBtn.setEnabled(True)

    def _widgetClose(self):
        self._idLineEdit.setEnabled(False)
        self._searchBtn.setEnabled(False)
        self._nameLineEdit.setEnabled(False)
        self._ageSpinBox.setEnabled(False)
        self._genderComboBox.setEnabled(False)
        self._diagnoseTextEdit.setEnabled(False)
        self._submitBtn.setEnabled(False)
        # self._addNewCaseBtn.setEnabled(False)

    def _widgetOpen(self):
        self._idLineEdit.setEnabled(True)
        self._searchBtn.setEnabled(True)
        self._nameLineEdit.setEnabled(True)
        self._ageSpinBox.setEnabled(True)
        self._genderComboBox.setEnabled(True)
        self._diagnoseTextEdit.setEnabled(True)
        self._submitBtn.setEnabled(True)
        # self._addNewCaseBtn.setEnabled(True)

    @pyqtSlot()
    def _resetUI(self):
        self._widgetInit()
        self._oldCaseTextEdit.clear()
        self._diagnoseTextEdit.clear()
        self._idLineEdit.setText('d286de4e-3b1c-457c-9259-e3b599c92433')
        self._ageSpinBox.setValue(0)
        self._genderComboBox.setCurrentText('男')
        self._isEditing = False
        self._isSearched = False
        self._addNewCaseBtn.setText('新建病历')

    @pyqtSlot()
    def _onAddNewCaseClicked(self):
        # TODO: 判断有点问题
        # TODO: 当查询后应该显示重置而非新建病历
        if self._isEditing or self._isSearched:
            msgBox = MessageBox('提示', '您将要进行的操作将清空全部数据，是否继续？', self)
            msgBox.show()
            msgBox.yesSignal.connect(self._resetUI)
        else:
            self._isEditing = True
            self._addNewCaseBtn.setText('重置')
            self._widgetOpen()
            # self._addNewCaseBtn.setEnabled(False)
            self._idLineEdit.setEnabled(False)
            self._searchBtn.setEnabled(False)
            self._idLineEdit.setText(str(uuid.uuid4()))

    @pyqtSlot()
    def _onSearchBtnClicked(self):
        self._widgetClose()
        self._diagnoseTextEdit.setEnabled(True)
        # 读取uuid
        _patientUUID = self._idLineEdit.text()
        if _patientUUID == '':
            InfoBar(
                InfoBarIcon.WARNING,
                '提示',
                'uuid不得为空！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            self._widgetInit()
            return
        # 从数据库读入数据
        try:
            res = self._mysql.queryCaseRecord(_patientUUID)
        except SqlCannotConnectException:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '无法连接数据库\n请确保数据库开启且配置信息准确！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            self._widgetInit()
            return
        except SqlNoMatchException:
            # 弹窗询问是否需要新建病历
            # 按确认按钮，触发新建档案操作
            # 按取消按钮，恢复UI为默认设置
            msgBox = MessageBox('提示', '未查询到该UUID对应患者信息，可能该患者信息未录入系统。是否要为该患者新建病历档案？', self)
            msgBox.yesSignal.connect(lambda: self._addNewCaseBtn.clicked.emit())
            msgBox.cancelSignal.connect(lambda: self._widgetInit())
            msgBox.show()
            pass
        except SqlException as e:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                str(e),
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            self._widgetInit()
        else:
            self._isSearched = True
            # (record, datatime, doctor, patient, gender, age)
            patientName = res['name']

            age = res['age']
            gender = '男' if res['gender'] == 'male' else '女'
            self._nameLineEdit.setText(patientName)
            self._ageSpinBox.setValue(int(age))
            self._genderComboBox.setCurrentText(gender)
            allRecord = ''
            # 用html展示数据
            for record in res['records']:
                allRecord += f'''<br/><p align="center">时间：{record[1]}\t责任医师：{record[2]}</p><hr/><br/>{record[0]}\n\n<hr/><br/>'''
            self._oldCaseTextEdit.setHtml(allRecord)
            self._submitBtn.setEnabled(True)

    @pyqtSlot()
    def _onSubmitBtnClicked(self):
        _patientUUID = self._idLineEdit.text()
        name = self._nameLineEdit.text()
        age = self._ageSpinBox.value()
        gender = 'male' if self._genderComboBox.currentText() == '男' else 'female'
        oldInfo = self._oldCaseTextEdit.toPlainText()
        record = self._diagnoseTextEdit.toPlainText()
        if _patientUUID == '' or name == '' or record == '':
            InfoBar(
                InfoBarIcon.WARNING,
                '提示',
                '诊断信息不可为空',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        if not oldInfo == '':
            # 向case表插入一条新纪录
            try:
                if self._mysql.addNewCase(
                    record,
                    self._uuid,
                    _patientUUID
                ):
                    self._resetUI()
                    InfoBar(
                        InfoBarIcon.SUCCESS,
                        '',
                        '提交成功！',
                        Qt.Orientation.Horizontal,
                        isClosable=False,
                        duration=3000,
                        parent=self
                    ).show()
            except SqlException or RuntimeException as e:
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
        else:
            # 向case表和patient表插入新纪录
            try:
                isAddPatient = self._mysql.addNewPatient(
                    _patientUUID,
                    name,
                    gender,
                    age
                )
                isAddCase = self._mysql.addNewCase(
                    record,
                    self._uuid,
                    _patientUUID
                )
            except SqlException or RuntimeException as e:
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
            else:
                if isAddPatient and isAddCase:
                    self._resetUI()
                    InfoBar(
                        InfoBarIcon.SUCCESS,
                        '',
                        '提交成功！',
                        Qt.Orientation.Horizontal,
                        isClosable=False,
                        duration=3000,
                        parent=self
                    ).show()

    def _bindSlot(self):
        self._searchBtn.clicked.connect(self._onSearchBtnClicked)
        self._submitBtn.clicked.connect(self._onSubmitBtnClicked)
        self._addNewCaseBtn.clicked.connect(self._onAddNewCaseClicked)
        pass

    def _setQss(self):
        self.setStyleSheet('''
            QTextEdit#oldCaseTextEdit, #diagnoseTextEdit{
                border: 2px solid rgb(0,159,170);
                background-color: white;
                border-radius: 10px;
                padding: 1px 18px 1px 3px;
                selection-background-color: rgb(0,159,170);
            }
            SettingInterface, #scrollWidget {
                background-color: transparent;
            }
            
            QScrollArea {
                background-color: transparent;
                border: none;
            }
     
            /* 滚动条 */
            QScrollBar {
                background: transparent;
                width: 4px;
                margin-top: 32px;
                margin-bottom: 0;
                padding-right: 2px;
            }
            
            /*隐藏上箭头*/
            QScrollBar::sub-line {
                background: transparent;
            }
            
            /*隐藏下箭头*/
            QScrollBar::add-line {
                background: transparent;
            }
            
            QScrollBar::handle {
                background: rgb(122, 122, 122);
                border: 2px solid rgb(128, 128, 128);
                border-radius: 1px;
                min-height: 32px;
            }
            
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        ''')

    def __del__(self):
        self._mysql.__del__()
