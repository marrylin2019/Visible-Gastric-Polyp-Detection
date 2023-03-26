import sys
import unittest

from PyQt6.QtWidgets import QApplication
from yolosegmention.beans.exit import exit_process

from yolosegmention.gui.modules.preview import PreViewLabelsUI


class MyTestCase(unittest.TestCase):
    def test_something(self):
        app = QApplication(sys.argv)
        mainWindow = PreViewLabelsUI()
        mainWindow.show()
        # 针对不同退出码进行处理
        exit_process(app.exec())


if __name__ == '__main__':
    unittest.main()
