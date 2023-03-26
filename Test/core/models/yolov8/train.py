import unittest

from yolosegmention.core.models.yolov8.train import train


class MyTestCase(unittest.TestCase):
    def test_something(self):
        train(r'D:\Program\Python\Graduation-Project-Fluent\yolosegmention\core\models\yolov8\pre-weights\yolov8n-seg.pt',
              r'D:\Program\Python\Graduation-Project-Fluent\data\Polyp-SEG\Polyp-SEG.yaml',
              batch=10, epochs=1)


if __name__ == '__main__':
    unittest.main()
