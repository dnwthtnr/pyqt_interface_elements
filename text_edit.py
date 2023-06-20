from pyqt_interface_elements import constants, base_layouts, base_widgets, base_windows, icons
from PySide2 import QtCore, QtWidgets, QtGui
from functools import partial
import os
import copy


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

class LargeListDisplay(base_widgets.TextEdit):
    list_ending_seperator = "{"
    list_beginning_seperator = "}"
    item_seperator = "}:|:{"

    def __init__(self, _list=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list(self):
        _trimmed_string = self.toPlainText()[0:-2]
        print(_trimmed_string)
        return _trimmed_string.split(self.item_seperator)

    def setList(self, _list, *args, **kwargs):
        if not isinstance(_list, list) or len(_list) < 1:
            return
        _list_string = copy.deepcopy(self.item_seperator)
        _list_string.join(_list)

        _full_string = self.list_beginning_seperator + _list_string + self.list_ending_seperator

        self.setText(_full_string)

