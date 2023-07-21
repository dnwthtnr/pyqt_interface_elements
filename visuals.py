from pyqt_interface_elements import base_widgets, base_layouts
import time

from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import constants
import os

r"Q:\__packages\_GitHub\pyqt_interface_elements\resources\animations\load00.gif"

# def get_animation_icons(file_name):
#     _path = os.path.join("", constants.animation_local_directory, file_name)
#
#     _icon_list = []
#     for _image in sorted(os.listdir(_path)):
#         _icon = QtGui.QIcon(_path)
#         _icon_list.append(_icon)
#
#     return _icon_list
#
# class LoadingRing(base_widgets.Tool_Button):
#
#     def __init__(self):
#         super().__init__()
#
#     def start_animation(self):
#
#         _icons = get_animation_icons("ring_load")
#
#         _amount = len(_icons)
#         _count = 0
#         while self.isVisible() is True:
#             print(_count)
#             self.setIcon(_icons[_count])
#             _count += 1
#             if _count == _amount:
#                 _count = 0
#             time.sleep(.3)

def get_gif(name):
    _label = QtWidgets.QLabel()

    _mov = QtGui.QMovie(r"Q:\__packages\_GitHub\pyqt_interface_elements\resources\animations\loads.gif")


    _label.setMovie(_mov)
    return _label


loading_wheel = get_gif('loads')

if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _window = base_layouts.VerticalLayout()
        _label = QtWidgets.QLabel()

        _mov = QtGui.QMovie(r"Q:\__packages\_GitHub\pyqt_interface_elements\resources\animations\loads.gif")


        _label.setMovie(_mov)
        _window.addWidget(_label)
        _window.show()
        _mov.start()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())
