from pyqt_interface_elements import base_widgets, base_layouts
import time

from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import constants
import os
def get_animation_icons(file_name):
    _path = os.path.join("", constants.animation_local_directory, file_name)

    _icon_list = []
    for _image in sorted(os.listdir(_path)):
        _icon = QtGui.QIcon(_path)
        _icon_list.append(_icon)

    return _icon_list

class LoadingRing(base_widgets.Tool_Button):
    
    def __init__(self):
        super().__init__()

    def start_animation(self):

        _icons = get_animation_icons("ring_load")

        _amount = len(_icons)
        _count = 0
        while self.isVisible() is True:
            print(_count)
            self.setIcon(_icons[_count])
            _count += 1
            if _count == _amount:
                _count = 0
            time.sleep(.3)


if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _window = base_layouts.VerticalLayout()

        _icons = LoadingRing()
        _window.addWidget(_icons)

        _window.show()
        _icons.start_animation()

        time.sleep(5)
        _icons.hide()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())
