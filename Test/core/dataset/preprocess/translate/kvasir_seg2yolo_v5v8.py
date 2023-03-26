import os.path
import shutil
import unittest
from yolosegmention.core.dataset.preprocess.translate.kvasir_seg2yolo_v5v8 import Translator


class MyTestCase(unittest.TestCase):
    def test_something_(self):
        path = r'D:\Program\Python\Graduation-Project-Fluent\data\Kvasir-SEG-10\kavsir_bboxes.json'
        mask_path = r'D:\Program\Python\Graduation-Project-Fluent\data\Kvasir-SEG-10\masks'
        result_path = r'D:\Program\Python\Graduation-Project-Fluent\data\tmpDataset\labels'
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        translator = Translator(path)
        for file_name in translator.file_names:
            translator.process(os.path.join(mask_path, file_name + '.png'))
        translator.write_all_to_file(result_path, translator.file_names)

        if os.path.exists(result_path):
            shutil.rmtree(os.path.split(result_path)[0])


if __name__ == '__main__':
    unittest.main()
