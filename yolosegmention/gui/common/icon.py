"""
@Project ：Graduation-Project-Fluent 
@File    ：icon.py
@Author  ：X0RB64
@Date    ：2023/03/30 18:26 
"""
# from os.path import dirname, split, join
# from enum import Enum
# from qfluentwidgets import getIconColor, Theme, FluentIconBase
#
#
# class Icon(FluentIconBase, Enum):
#     """ Custom icons """
#
#     PREVIOUS = 'chevron-left'
#     NEXT = 'chevron-right'
#
#     def path(self, theme=Theme.AUTO):
#         if theme == Theme.AUTO:
#             c = getIconColor()
#         else:
#             c = "white" if theme == Theme.DARK else "black"
#
#         return join(split(dirname(__file__))[0], 'Resources',  f'{self.value}_{c}.svg')
