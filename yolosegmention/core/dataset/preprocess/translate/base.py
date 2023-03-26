"""
@Project ：Graduation-Project-Fluent 
@File    ：base.py
@Author  ：X0RB64
@Date    ：2023/03/24 18:48 
"""
from abc import ABC, abstractmethod

from yolosegmention.core.dataset.preprocess.parse.base import BaseGetter


class BaseTranslator(ABC):
    @property
    def configPath(self) -> str:
        return self._configPath

    @property
    @abstractmethod
    def getter(self) -> BaseGetter:
        pass

    def __init__(self, configPath: str):
        super().__init__()
        self._configPath = configPath

    @abstractmethod
    def process(self, *args, **kwargs):
        pass
