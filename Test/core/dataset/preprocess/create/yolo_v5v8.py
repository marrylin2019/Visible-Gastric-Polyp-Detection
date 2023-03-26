import os.path
import shutil
import unittest
from yolosegmention.core.dataset.preprocess.create.yolo_v5v8 import Creator
from yolosegmention.exceptions.exceptions import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        PATHS = {
            # 根路径
            'ROOT': r'D:\Program\Python\Graduation-Project-Fluent\data',

            # 源数据集信息
            # 源数据文件夹名
            'RAW_DATASET_FOLDER': 'Kvasir-SEG-10',
            # 掩膜图片文件夹名
            'MASK_PIC_FOLDER': 'masks',
            # 源图片文件夹名
            'RAW_PIC_FOLDER': 'images',
            # json文件名
            'JSON_NAME': r'kavsir_bboxes.json',

            # 目标数据集信息
            'DATASET_FOLDER': 'Polyp-SEG',
            'YAML_NAME': r'Polyp-SEG.yaml',
        }

        try:
            creator = Creator(PATHS)
            for file_name in creator.file_names:
                creator.process(file_name + '.png')
            for i in range(3):
                creator.write(i)
        except FileException or RuntimeException as e:
            print(e)
            dataset_path = os.path.join(PATHS['ROOT'], PATHS['DATASET_PATH'])
            if os.path.exists(dataset_path):
                shutil.rmtree(dataset_path)
            self.assertEqual(True, False)
        except Exception as e:
            print(e)
            dataset_path = os.path.join(PATHS['ROOT'], PATHS['DATASET_PATH'])
            if os.path.exists(dataset_path):
                shutil.rmtree(dataset_path)
            self.assertEqual(True, False)
        # finally:
        #     dataset_path = os.path.join(PATHS['ROOT'], PATHS['DATASET_PATH'])
        #     if os.path.exists(dataset_path):
        #         shutil.rmtree(dataset_path)


if __name__ == '__main__':
    unittest.main()
