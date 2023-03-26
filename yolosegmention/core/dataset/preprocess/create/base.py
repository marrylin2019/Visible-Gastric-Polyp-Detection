"""
@Project ：Graduation-Project-Fluent 
@File    ：base.py
@Author  ：X0RB64
@Date    ：2023/03/24 21:22 
"""
from abc import ABC, abstractmethod

from ..translate.base import BaseTranslator


class BaseCreator(ABC):
    @property
    @abstractmethod
    def translator(self) -> BaseTranslator:
        pass

    @property
    def configPath(self) -> str:
        return self._configPath

    def __init__(self, configPath: str):
        super().__init__()
        self._configPath = configPath

    @abstractmethod
    def process(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def write(self, *args, **kwargs) -> None:
        pass
