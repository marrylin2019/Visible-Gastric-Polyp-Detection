"""
@Project ：Graduation-Project-Fluent 
@File    ：__init__.py.py
@Author  ：X0RB64
@Date    ：2023/03/24 17:45 
"""
from os.path import normpath, join, dirname

YOLOv8n_SEG_PATH = normpath(join(dirname(__file__), 'pre-weights/yolov8n-seg.pt'))
