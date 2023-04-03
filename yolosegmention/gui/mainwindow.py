"""
@Project ：Graduation-Project-Fluent 
@File    ：mainwindow.py
@Author  ：X0RB64
@Date    ：2023/04/03 19:11 
"""
import multiprocessing
from pathlib import Path

from yolosegmention.gui.app.view.main_window import MainWindow


def mainWindow(permission: str, nickname: str, _uuid: str):
    multiprocessing.freeze_support()
    # create main window
    w = MainWindow(Path(__file__).parent, nickname, _uuid, permission)
    w.show()
