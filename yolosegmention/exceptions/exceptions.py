"""
@Project ：Graduation-Project-Fluent 
@File    ：exceptions.py
@Author  ：X0RB64
@Date    ：2023/03/24 15:44 
"""
import traceback


class FileException(Exception):
    def __init__(self, info: str, should_trace_back: bool = False):
        super().__init__()
        if not (info == '' or info.endswith('\n')):
            self.__info = info + '\n'
        else:
            self.__info = info
        self.__should_trace_back = should_trace_back
        self.__trace_back_info = traceback.format_exc()

    def __str__(self):
        return self.__info + (lambda: self.__trace_back_info if self.__should_trace_back else "")()


class RuntimeException(Exception):
    def __init__(self, info: str = ''):
        super().__init__()
        if not (info == '' or info.endswith('\n')):
            self.__info = info + '\n'
        else:
            self.__info = info
        self.__trace_back_info = traceback.format_exc()

    def __str__(self):
        return self.__trace_back_info + self.__info


class SqlException(Exception):
    def __init__(self, info: str):
        super().__init__()
        self._info = info

    def __str__(self):
        return self._info


class SqlCannotConnectException(Exception):
    def __init__(self):
        super().__init__()


class SqlNoMatchException(Exception):
    def __init__(self):
        super().__init__()
