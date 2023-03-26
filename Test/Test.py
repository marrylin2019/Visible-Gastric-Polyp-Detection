"""
@Project ：Graduation-Project-Fluent 
@File    ：Test.py
@Author  ：X0RB64
@Date    ：2023/03/25 18:08 
"""
import sys

from PyQt6.QtWidgets import QWidget, QApplication, QPushButton
from yolosegmention.libs.qfluentwidgets import FluentIcon
from yolosegmention.libs.qfluentwidgets.components.widgets.button import PushButton


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(160, 80)
        self.btn = QPushButton()
        self.btn.setStyleSheet()
        self.btn.move(50, 24)
        self.btn.clicked.connect(self.onClicked)

    def onClicked(self):
        print('Button was clicked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
