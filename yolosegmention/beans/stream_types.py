"""
@Project ：Graduation-Project-Fluent 
@File    ：stream_types.py
@Author  ：X0RB64
@Date    ：2023/04/03 14:15 
"""
from enum import Enum


class StreamTypes(Enum):
    PICTURE = '图片'
    VIDEO = '视频'
    STREAM = '视频流'


PATTERNS = {
    StreamTypes.PICTURE: r'.*?((\.png)|(\.jpg))',
    StreamTypes.VIDEO: r'.*?((\.wmv)|(\.avi)|(\.mp4)|(\.mov))',
    StreamTypes.STREAM: r'rtmp:\/\/',
}