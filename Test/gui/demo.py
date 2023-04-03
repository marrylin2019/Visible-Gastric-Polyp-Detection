"""
@Project ：Graduation-Project-Fluent 
@File    ：demo.py
@Author  ：X0RB64
@Date    ：2023/03/30 23:35 
"""
import multiprocessing
# coding:utf-8
import os
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from yolosegmention.gui.app.common.config import cfg
from yolosegmention.gui.app.view.main_window import MainWindow


# # enable dpi scale
# if cfg.get(cfg.dpiScale) != "Auto":
#     os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
#     os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

def adminUI(nickname: str = '', _uuid: str = ''):
    multiprocessing.freeze_support()
    # create application
    # app = QApplication(sys.argv)
    # app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # create main window
    w = MainWindow(Path(__file__).parent, nickname, _uuid)
    # w.setWindowIcon(QIcon(r'D:\Program\Python\Graduation-Project-Fluent\yolosegmention\gui\app\resource\images\logo.png'))
    w.show()

    # app.exec()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # create main window
    w = MainWindow(Path(__file__).parent, '刘大夫', '050d78d0-31be-4799-b79e-f2e86fdf5123')
    # w.setWindowIcon(QIcon(r'D:\Program\Python\Graduation-Project-Fluent\yolosegmention\gui\app\resource\images\logo.png'))
    w.show()

    app.exec()
