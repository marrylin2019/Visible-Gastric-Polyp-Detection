# coding: utf-8
import os.path
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):

    HOME = "Home"
    CHAT = "Chat"
    CODE = "Code"
    MENU = "Menu"
    SHUT = 'Shut'
    CASE = 'Case'
    PLAY = 'Play'
    NEXT = 'chevron-right'
    PAUSE = 'Pause'
    ALBUM = "Album"
    BATCH = 'Batch'
    EPOCH = 'Epoch'
    SCROLL = "Scroll"
    LAYOUT = "Layout"
    PREDICT = 'Predict'
    MESSAGE = "Message"
    PREVIEW = 'Preview'
    CHECKBOX = "CheckBox"
    DOCUMENT = "Document"
    MINIMIZE = "Minimize"
    PREVIOUS = 'chevron-left'
    CONSTRACT = "Constract"
    PREPROCESS = 'Preprocess'
    TRAIN_MODEL = 'TrainModel'
    DATASET_FORMAT = 'Format'

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return os.path.join(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'resource'), f"images/icons/{self.value}_{c}.svg")
