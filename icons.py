
from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import constants
import os
def get_icon(file_name):
    _path = os.path.join("", constants.icon_local_directory, file_name)
    return QtGui.QIcon(_path)

open_file = get_icon("open_file.svg")
close = get_icon("close.svg")
save = get_icon("save.svg")

down_arrow = get_icon("down_arrow.svg")
up_arrow = get_icon("up_arrow.svg")

checkbox_checked = get_icon("checkbox_checked.svg")
checkbox_unchecked = get_icon("checkbox_unchecked.svg")
