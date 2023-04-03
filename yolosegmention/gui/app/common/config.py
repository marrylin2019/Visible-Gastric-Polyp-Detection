# coding:utf-8
from enum import Enum

from qfluentwidgets import (qconfig, QConfig, RangeConfigItem, OptionsConfigItem, ConfigItem, RangeValidator,
                                 OptionsValidator, EnumSerializer, FolderValidator)

from yolosegmention.beans import DatasetTypes
from yolosegmention.beans.dataset_model_types import ModelTypes


class Config(QConfig):
    """ Config of application """

    # transform
    transformSrcFormat = OptionsConfigItem(
        "Transform", "SrcFormat", DatasetTypes.KVASIR_SEG, OptionsValidator(DatasetTypes), EnumSerializer(DatasetTypes))
    transformDestFormat = OptionsConfigItem(
        "Transform", "DestFormat", DatasetTypes.YOLOv8, OptionsValidator(DatasetTypes), EnumSerializer(DatasetTypes))
    transformSrcFolder = ConfigItem(
        "Transform", "SrcFolder", './', FolderValidator())
    transformDestFolder = ConfigItem(
        "Transform", "DestFolder", "./", FolderValidator())

    # train
    trainModelFormat = OptionsConfigItem(
        'Train', 'ModelFormat', ModelTypes.YOLOv8_SEGMENT, OptionsValidator(ModelTypes), EnumSerializer(ModelTypes))
    trainDatasetFolder = ConfigItem(
        "Train", "DatasetFolder", './')
    trainPreWeightFolder = ConfigItem(
        "Train", "PreWeightFolder", './')
    trainBatch = OptionsConfigItem(
        "Train", "Batch", 16, OptionsValidator([8, 16, 32]))
    trainEpochs = RangeConfigItem(
        "Train", "Epochs", 10, RangeValidator(1, 150))



    # # folders
    # musicFolders = ConfigItem(
    #     "Folders", "LocalMusic", [], FolderListValidator())
    # downloadFolder = ConfigItem(
    #     "Folders", "Download", "app/download", FolderValidator())
    #
    # # main window
    # dpiScale = OptionsConfigItem(
    #     "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    #
    # # Material
    # blurRadius  = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))
    #
    # # software update
    # checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


# YEAR = 2023
# AUTHOR = "zhiyiYo"
# VERSION = "v0.4.2"
# HELP_URL = "https://pyqt-fluent-widgets.readthedocs.io"
# REPO_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
# EXAMPLE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples"
# FEEDBACK_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues"
# RELEASE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases/latest"


cfg = Config()
qconfig.load('app/config/config.json', cfg)