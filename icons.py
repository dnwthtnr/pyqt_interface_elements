
from PySide2 import QtCore, QtWidgets, QtGui
from interface_elements import constants
import os

def get_icon(file_name):
    _path = os.path.join("", constants.icon_local_directory, file_name)
    print(os.path.abspath(_path))
    return QtGui.QIcon(_path)

open_file = get_icon("open_file.svg")
print(open_file)
