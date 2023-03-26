"""
@Project ：Graduation-Project-Fluent 
@File    ：base.py
@Author  ：X0RB64
@Date    ：2023/03/24 18:30 
"""
from abc import ABC, abstractmethod


class BaseGetter(ABC):
    @property
    def configPath(self) -> str:
        return self._configPath

    def __init__(self, configPath: str):
        super().__init__()
        self._configPath = configPath

    @abstractmethod
    def read(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def preprocess(self, *args, **kwargs) -> None:
        pass
