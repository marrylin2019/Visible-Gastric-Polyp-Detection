"""
@Project ：Graduation-Project-Fluent 
@File    ：main.py
@Author  ：X0RB64
@Date    ：2023/04/03 19:08 
"""
import sys
from yolosegmention.gui.app.view.login import Login
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
demo = Login()
demo.show()
sys.exit(app.exec())
