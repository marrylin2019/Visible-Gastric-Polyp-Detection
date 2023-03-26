import os
import unittest

from yolosegmention.core.dataset import generate


class MyTestCase(unittest.TestCase):
    def test_something(self):
        picture_path = r"D:\Program\Python\Graduation-Project-Fluent\data\Kvasir-SEG-10/masks"
        text_path = r"D:\Program\Python\Graduation-Project-Fluent\data\dataset/labels/train/"
        result_path = r'D:\Program\Python\Graduation-Project-Fluent\data\dataset/labels_validate'
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        generate(picture_path, text_path, result_path, 7, {'0': (0, 255, 255)})


if __name__ == '__main__':
    unittest.main()
