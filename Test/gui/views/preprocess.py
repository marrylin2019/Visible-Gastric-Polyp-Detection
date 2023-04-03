import sys
import unittest

from PyQt6.QtWidgets import QApplication

from yolosegmention.beans import exit_process
from yolosegmention.gui.views.preprocess import PreprocessUI


class MyTestCase(unittest.TestCase):
    def test_something(self):
        app = QApplication(sys.argv)
        mainWindow = PreprocessUI()
        mainWindow.show()
        # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6', palette=LightPalette()))
        # 针对不同退出码进行处理
        exit_process(app.exec())


if __name__ == '__main__':
    unittest.main()
