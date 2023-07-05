from pyqt_interface_elements import constants, base_layouts, base_widgets, base_windows, icons, buttons, line_edits
from PySide2 import QtCore, QtWidgets, QtGui
from functools import partial
import os


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class DropdownLayout(base_layouts.VerticalScrollArea):
    
    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(margins=margins, spacing=spacing)
        self.setWindowFlags(QtCore.Qt.Popup)



class DropdownBar(base_layouts.HorizontalLayout):
    dropdownClicked = QtCore.Signal(bool)   # True if dropped down

    def finish_initialization(self):

        self.dropdown_button = self._build_button()
        self.selected_label = self._build_label()

        if self.dropdown_on_left is True:
            self.addWidget(self.dropdown_button, alignment=constants.align_left)
            self.addWidget(self.selected_label)
        else:
            self.addWidget(self.selected_label)
            self.addWidget(self.dropdown_button, alignment=constants.align_right)


    def __init__(self, dropdown_on_left=False, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(margins=margins, spacing=spacing)
        self.dropdown_on_left = dropdown_on_left
        self.finish_initialization()

    def bottom_left_global_point(self):
        _dropdown_bar_geometry = self.rect()
        _dropdown_bottom_left_point_LOCAL = _dropdown_bar_geometry.bottomLeft()

        _parent = self.parent()
        if _parent is None:
            return self.mapToParent(_dropdown_bottom_left_point_LOCAL)
        else:
            _dropdown_bottom_left_point_GLOBAL = _parent.mapToGlobal(self.mapToParent(_dropdown_bottom_left_point_LOCAL))
            return _dropdown_bottom_left_point_GLOBAL

    # region Label
    def _build_label(self):
        _label = base_widgets.Line_Edit()

        return _label

    def setText(self, text):
        self.selected_label.setText(text)

    # region Button

    def _build_button(self):
        _button = buttons.DropdownToggleButton()
        _button.clicked.connect(self._emit_dropdown_clicked)

        return _button

    @QtCore.Slot()
    def _emit_dropdown_clicked(self):
        self.dropdownClicked.emit(self.dropdown_button.enabledState)


class Dropdown(DropdownBar):

    def __init__(self):
        super().__init__()
        self.dropdownClicked.connect(self.dropdown)
        self.dropdown_layout = DropdownLayout()
        _label = base_widgets.Label(text='asdasd')
        self.dropdown_layout.addWidget(_label)

    def dropdown(self, dropState):
        if dropState is True:
            # dropped
            self.show_dropdown()
        else:
            self.dropdown_layout.hide()

    def show_dropdown(self):
        self.dropdown_layout.show()
        _point = self.bottom_left_global_point()
        self.dropdown_layout.move(_point)








if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _window = Dropdown()

        _window.show()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())
