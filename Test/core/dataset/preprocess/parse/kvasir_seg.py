import os
import unittest
from yolosegmention.core.dataset.preprocess.parse.kvasir_seg import Getter
from yolosegmention.core.dataset.preprocess.common.utils import standardise_file_name


class MyTestCase(unittest.TestCase):
    def test_sonmething_Kvasir_SEG_10(self):
        path = r'D:\Program\Python\Graduation-Project-Fluent\data\Kvasir-SEG-10\kavsir_bboxes.json'
        getter = Getter(path)
        self.assertEqual(getter.file_name_list, [standardise_file_name(fileName) for fileName in os.listdir(os.path.join(os.path.dirname(path), 'images'))])
        # TODO: 测试其他函数返回值


if __name__ == '__main__':
    unittest.main()
