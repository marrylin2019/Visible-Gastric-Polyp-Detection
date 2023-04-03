# coding: utf-8
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationInterface, NavigationItemPostion, MessageBox,
                            isDarkTheme, PopUpAniStackedWidget, InfoBar, InfoBarIcon)

from .case_interface import CaseInterface
from .predict_interface import PredictInterface
from .train_interface import TrainUI
from ..common.icon import Icon
from qframelesswindow import FramelessWindow

from .title_bar import CustomTitleBar
from ..components.avatar_widget import AvatarWidget
from .preprocess_interface import TransformInterface
from .preview_interface import PreviewLabelsUI


class StackedWidget(QFrame):
    """ Stacked widget """
    currentWidgetChanged = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget, popOut=False):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.Type.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class MainWindow(FramelessWindow):

    def __init__(self, root: Path, nickname: str, _uuid: str, permission: str):
        super().__init__()
        self.isAdmin = permission == 'admin'
        self._root = root
        self.nickname = nickname
        self._uuid = _uuid
        self._RESOURCES_PATH = Path(__file__).parent.parent.joinpath('resource')
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        # create sub interface
        if self.isAdmin:
            self.transformInterface = TransformInterface(self)
            self.previewInterface = PreviewLabelsUI(self)
            self.trainInterface = TrainUI(self)
        else:
            self.caseInterface = CaseInterface(self.nickname, self._uuid, self)
            self.predictInterface = PredictInterface(self._root, self)
        # self.homeInterface = HomeInterface(self)
        # self.basicInputInterface = BasicInputInterface(self)
        # self.dialogInterface = DialogInterface(self)
        # self.layoutInterface = LayoutInterface(self)
        # self.menuInterface = MenuInterface(self)
        # self.materialInterface = MaterialInterface(self)
        # self.scrollInterface = ScrollInterface(self)
        # self.statusInfoInterface = StatusInfoInterface(self)
        # self.settingInterface = SettingInterface(self)

        if self.isAdmin:
            self.stackWidget.addWidget(self.transformInterface)
            self.stackWidget.addWidget(self.previewInterface)
            self.stackWidget.addWidget(self.trainInterface)
        else:
            self.stackWidget.addWidget(self.caseInterface)
            self.stackWidget.addWidget(self.predictInterface)
        # self.stackWidget.addWidget(self.homeInterface)
        # self.stackWidget.addWidget(self.basicInputInterface)
        # self.stackWidget.addWidget(self.dialogInterface)
        # self.stackWidget.addWidget(self.layoutInterface)
        # self.stackWidget.addWidget(self.materialInterface)
        # self.stackWidget.addWidget(self.menuInterface)
        # self.stackWidget.addWidget(self.scrollInterface)
        # self.stackWidget.addWidget(self.statusInfoInterface)
        # self.stackWidget.addWidget(self.settingInterface)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        if self.isAdmin:
            self.transformInterface.setObjectName('transformInterface')
            self.previewInterface.setObjectName('previewInterface')
            self.trainInterface.setObjectName('trainInterface')
        else:
            self.caseInterface.setObjectName('caseInterface')
            self.predictInterface.setObjectName('predictInterface')
        # self.homeInterface.setObjectName('homeInterface')
        # self.basicInputInterface.setObjectName('basicInputInterface')
        # self.dialogInterface.setObjectName('dialogInterface')
        # self.layoutInterface.setObjectName('layoutInterface')
        # self.menuInterface.setObjectName('menuInterface')
        # self.materialInterface.setObjectName('materialInterface')
        # self.statusInfoInterface.setObjectName('statusInfoInterface')
        # self.scrollInterface.setObjectName('scrollInterface')
        # self.settingInterface.setObjectName('settingsInterface')

        # add navigation items
        if self.isAdmin:
            self.navigationInterface.addItem(
                routeKey=self.transformInterface.objectName(),
                icon=Icon.PREPROCESS,
                text='数据集格式转换',
                onClick=lambda t: self.switchTo(self.transformInterface, t),
                position=NavigationItemPostion.SCROLL
            )
            self.navigationInterface.addItem(
                routeKey=self.previewInterface.objectName(),
                icon=Icon.PREVIEW,
                text='预览',
                onClick=lambda t: self.switchTo(self.previewInterface, t)
            )
            self.navigationInterface.addItem(
                routeKey=self.trainInterface.objectName(),
                icon=Icon.TRAIN_MODEL,
                text='训练',
                onClick=lambda t: self.switchTo(self.trainInterface, t)
            )
        else:
            self.navigationInterface.addItem(
                routeKey=self.caseInterface.objectName(),
                icon=Icon.CASE,
                text='病历',
                onClick=lambda t: self.switchTo(self.caseInterface, t)
            )
            self.navigationInterface.addItem(
                routeKey=self.predictInterface.objectName(),
                icon=Icon.PREDICT,
                text='预测',
                onClick=lambda t: self.switchTo(self.predictInterface, t)
            )
        # self.navigationInterface.addItem(
        #     routeKey=self.homeInterface.objectName(),
        #     icon=Icon.HOME,
        #     text='Home',
        #     onClick=lambda t: self.switchTo(self.homeInterface, t)
        # )
        # self.navigationInterface.addSeparator()
        #
        # self.navigationInterface.addItem(
        #     routeKey=self.basicInputInterface.objectName(),
        #     icon=Icon.CHECKBOX,
        #     text='Basic input',
        #     onClick=lambda t: self.switchTo(self.basicInputInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )
        # self.navigationInterface.addItem(
        #     routeKey=self.dialogInterface.objectName(),
        #     icon=Icon.MESSAGE,
        #     text='Dialogs',
        #     onClick=lambda t: self.switchTo(self.dialogInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )
        # self.navigationInterface.addItem(
        #     routeKey=self.layoutInterface.objectName(),
        #     icon=Icon.LAYOUT,
        #     text='Layout',
        #     onClick=lambda t: self.switchTo(self.layoutInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )
        # self.navigationInterface.addItem(
        #     routeKey=self.materialInterface.objectName(),
        #     icon=FIF.PALETTE,
        #     text='Material'),
        #     onClick=lambda t: self.switchTo(self.materialInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )
        # self.navigationInterface.addItem(
        #     routeKey=self.menuInterface.objectName(),
        #     icon=Icon.MENU,
        #     text='Menus'),
        #     onClick=lambda t: self.switchTo(self.menuInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )
        # self.navigationInterface.addItem(
        #     routeKey=self.scrollInterface.objectName(),
        #     icon=Icon.SCROLL,
        #     text='Scrolling'),
        #     onClick=lambda t: self.switchTo(self.scrollInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )
        # self.navigationInterface.addItem(
        #     routeKey=self.statusInfoInterface.objectName(),
        #     icon=Icon.CHAT,
        #     text='Status & info'),
        #     onClick=lambda t: self.switchTo(self.statusInfoInterface, t),
        #     position=NavigationItemPostion.SCROLL
        # )

        # add custom widget to bottom
        # 头像
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(str(self._RESOURCES_PATH.joinpath('images/profile.jpg')), self.nickname),
            onClick=self.showMessageBox,
            position=NavigationItemPostion.BOTTOM
        )

        # self.navigationInterface.addItem(
        #     routeKey=self.settingInterface.objectName(),
        #     icon=FIF.SETTING,
        #     text='Settings',
        #     onClick=lambda t: self.switchTo(self.settingInterface, t),
        #     position=NavigationItemPostion.BOTTOM
        # )

        # !IMPORTANT: don't forget to set the default route key if you enable the return button
        if self.isAdmin:
            self.navigationInterface.setDefaultRouteKey(
                self.transformInterface.objectName())
        else:
            self.navigationInterface.setDefaultRouteKey(
                self.caseInterface.objectName())

        self.stackWidget.currentWidgetChanged.connect(
            lambda w: self.navigationInterface.setCurrentItem(w.objectName()))
        if self.isAdmin:
            self.navigationInterface.setCurrentItem(
                self.transformInterface.objectName())
        else:
            self.navigationInterface.setCurrentItem(
                self.caseInterface.objectName())
        self.stackWidget.setCurrentIndex(0)

        InfoBar(
            InfoBarIcon.SUCCESS,
            '',
            '欢迎您' + ('' if self.nickname == '' else ', ') + self.nickname,
            Qt.Orientation.Horizontal,
            isClosable=False,
            duration=3000,
            parent=self.stackWidget
        ).show()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(580)
        self.setWindowIcon(QIcon(str(self._RESOURCES_PATH.joinpath('images/logo.png'))))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # cfg.themeChanged.connect(self.setQss)
        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(str(self._RESOURCES_PATH.joinpath(f'qss/{color}/main_window.qss')), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())

    def showMessageBox(self):
        w = MessageBox(
            '功能待完善',
            '计划是实现点击头像显示个人详细信息并允许修改个人信息',
            self
        )
        w.exec()
