"""
@Project ：GraduationProject 
@File    ：Exit.py
@Author  ：X0RB64
@Date    ：2023/02/28 21:20 
"""
import sys
import traceback

NORMAL_EXIT: int = 0
NOT_SAVE: int = -1
FILE_NOT_EXIST_ERR: int = -2
UNREACHABLE_ERR = -3
UNKNOWN_ERR: int = -100


def exit_process(code: int):
    if code == NORMAL_EXIT:
        print('正常退出')
        sys.exit(0)
    elif code == NOT_SAVE:
        print('文件未保存')
    elif code == FILE_NOT_EXIST_ERR:
        print('文件不存在异常')
    elif code == UNREACHABLE_ERR:
        print('不可达异常')
    elif None:
        pass
    elif None:
        pass
    elif None:
        pass
    elif None:
        pass
    elif None:
        pass
    elif code == UNKNOWN_ERR:
        print('未知错误')
    else:
        print('未知错误')
    traceback.print_stack()
    sys.exit(0)
