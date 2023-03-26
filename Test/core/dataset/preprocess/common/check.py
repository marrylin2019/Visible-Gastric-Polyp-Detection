import unittest

from yolosegmention.beans import DatasetTypes
from yolosegmention.core.dataset.preprocess.common.check import check


class MyTestCase(unittest.TestCase):
    def test_something_Yolov8(self):
        self.assertEqual(check(r'D:\Program\Python\Graduation-Project-Fluent\data\Polyp-SEG\Polyp-SEG.yaml', DatasetTypes.YOLOv8), (True, ''))

    def test_something_Kvasir_SEG(self):
        self.assertEqual(check(r'D:\Program\Python\Graduation-Project-Fluent\data\Kvasir-SEG-10\kavsir_bboxes.json', DatasetTypes.KVASIR_SEG),
                         (True, ''))


if __name__ == '__main__':
    unittest.main()
