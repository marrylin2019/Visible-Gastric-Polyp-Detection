# coding:utf-8
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QLabel, QWidget, QFrame, QPushButton

from gui.demo import adminUI
from yolosegmention.exceptions import SqlNoMatchException
from ..common.icon import Icon
from qfluentwidgets import LineEdit, PrimaryPushButton, InfoBar, InfoBarIcon
from yolosegmention.beans import exit
from ..common.mysql import Mysql
from ...mainwindow import mainWindow


class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._mysql = Mysql()
        self.m_position = None
        self.m_flag = None

        self._initUI()
        self._bindSlot()

    def _initUI(self):
        self.background = QFrame(self)
        self.title = QLabel('欢迎登录', parent=self.background)
        self.usernameLineEdit = LineEdit(parent=self.background)
        self.passwdLineEdit = LineEdit(parent=self.background)
        self.loginBtn = PrimaryPushButton('登录', parent=self.background)
        self.closeBtn = QPushButton(self.background)
        self.minBtn = QPushButton(self.background)

        self.background.setObjectName('background')
        self.closeBtn.setObjectName('closeBtn')
        self.minBtn.setObjectName('minBtn')

        self._setUI()

    def _setUI(self):
        self.background.setFixedSize(700, 500)
        self.closeBtn.setFixedSize(40, 40)
        self.minBtn.setFixedSize(40, 40)
        self.title.setFixedSize(200, 100)
        self.loginBtn.setFixedSize(400, 40)
        self.usernameLineEdit.setFixedSize(400, 40)
        self.passwdLineEdit.setFixedSize(400, 40)

        self.setContentsMargins(0, 0, 0, 0)
        self.background.setContentsMargins(0, 0, 0, 0)

        self.closeBtn.setIcon(Icon.SHUT.icon())
        self.minBtn.setIcon(Icon.MINIMIZE.icon())

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setFamily(u"\u5e7c\u5706")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)

        self.usernameLineEdit.setPlaceholderText('账号:')
        self.passwdLineEdit.setPlaceholderText('密码:')

        self.passwdLineEdit.setEchoMode(LineEdit.EchoMode.Password)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.background.setLayout(self.outsideLayout)
        self._setQss()

        self._setPos()

    def _setPos(self):
        # closeBtn移动到距离frame右边缘10px处
        closeBtnMoveLen = self.background.width() - self.closeBtn.width() - 30
        self.closeBtn.move(closeBtnMoveLen, 0)
        self.minBtn.move(closeBtnMoveLen - self.minBtn.width(), 0)

        # 所有控件水平居中
        titleXMoveLen = (self.background.width() - self.title.width()) // 2 + 15
        mainXMoveLen = (self.background.width() - self.loginBtn.width()) // 2 + 15
        loginBtnYMoveLen = self.background.height() - self.loginBtn.height() - 100
        passwordYMoveLen = loginBtnYMoveLen - self.passwdLineEdit.height() - 20
        usernameYMoveLen = passwordYMoveLen - self.usernameLineEdit.height() - 20
        titleYMoveLen = usernameYMoveLen - self.title.height() - 40
        self.loginBtn.move(mainXMoveLen, loginBtnYMoveLen)
        self.passwdLineEdit.move(mainXMoveLen, passwordYMoveLen)
        self.usernameLineEdit.move(mainXMoveLen, usernameYMoveLen)
        self.title.move(titleXMoveLen, titleYMoveLen)

    def _bindSlot(self):
        # 绑定槽函数
        self.closeBtn.clicked.connect(lambda: self.close())
        self.minBtn.clicked.connect(lambda: self.showMinimized())
        self.loginBtn.clicked.connect(self._onLoginBtnClicked)

    def _setQss(self):
        imgPath = str(Path(__file__).parent.parent.joinpath('resource/images/background.png')).replace("\\", "/")
        self.setStyleSheet(f'''
            QFrame{{
                border: 0px;
            }}
            QFrame#background{{
                border-image: url({imgPath});
                border-radius: 50px;
            }}
            QPushButton{{
                background: transparent;
                border: 0px;
            }}
            QPushButton:hover{{
                /* 选中按钮后按钮浮起 */
                padding-bottom:5px;
            }}
            QPushButton#closeBtn{{
                border-top-right-radius: 50px;
            }}
        ''')

    # 拖动窗口
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            self.m_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if Qt.MouseButton.LeftButton and self.m_flag:
            self.move(mouse_event.globalPosition().toPoint() - self.m_position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def _onLoginBtnClicked(self):
        # 核验数据是否为空
        username = self.usernameLineEdit.text()
        password = self.passwdLineEdit.text()
        if username == '' or password == '':
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '账号或密码不得为空',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return

        try:
            queryRes = Mysql().auth(username, password)
        except SqlNoMatchException:
            InfoBar(
                InfoBarIcon.ERROR,
                '警告',
                '无法连接数据库\n请确保数据库开启且配置信息准确！',
                Qt.Orientation.Horizontal,
                isClosable=False,
                duration=3000,
                parent=self
            ).show()
            return
        else:
            if not queryRes[0]:
                InfoBar(
                    InfoBarIcon.ERROR,
                    '警告',
                    '账号或密码错误',
                    Qt.Orientation.Horizontal,
                    isClosable=False,
                    duration=3000,
                    parent=self
                ).show()
                return
            mainWindow(queryRes[1], queryRes[2], queryRes[3])
            self.close()
            # if queryRes[1] == 'user':
            #     # 普通用户
            #     pass
            # elif queryRes[1] == 'admin':
            #     # 管理员
            #     # TODO: 测试代码，修改为主函数
            #     adminUI(queryRes[2], queryRes[3])
            #     self.close()
            #     pass
            # else:
            #     exit.exit_process(exit.UNREACHABLE_ERR)

