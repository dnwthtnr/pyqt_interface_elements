
from pyqt_interface_elements import constants, base_layouts, base_widgets, base_windows, icons
from PySide2 import QtCore, QtWidgets, QtGui
from functools import partial
import os


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class FloatLineEdit(base_widgets.Line_Edit):

    def __init__(self, value=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValue(value)
        self.setValidator(QtGui.QDoubleValidator())

    def value(self):
        return float(self.text())

    def setValue(self, value):
        self.setText(str(value))

class IntLineEdit(base_widgets.Line_Edit):

    def __init__(self, value=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValue(value)
        self.setValidator(QtGui.QIntValidator())

    def value(self):
        return float(self.text())

    def setValue(self, value):
        self.setText(str(value))


class File_Selection_Line_Edit(base_layouts.Horizontal_Layout):
    FileSelected = QtCore.Signal(str)
    textEdited = QtCore.Signal(str)

    def __init__(self, filepath, extension=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extension = extension
        self.filepath = filepath

        self.build_widget(filepath)

    def build_widget(self, filepath):
        self.line_edit = self.build_lineedit(filepath)
        self.button = self.build_button()

        self.addWidget(self.line_edit)
        self.addWidget(self.button, alignment=constants.align_right)


    def build_lineedit(self, filepath):
        filepath = filepath if os.path.exists(filepath) else ""
        _line_edit = base_widgets.Line_Edit(text=filepath)
        _line_edit.textEdited.connect(self.textEdited.emit)
        self.FileSelected.connect(_line_edit.setText)
        return _line_edit

    def build_button(self):
        _button = base_widgets.Tool_Button()
        _button.setIcon(icons.open_file)
        _button.clicked.connect(self.open_file_dialogue)
        return _button

    def open_file_dialogue(self):
        _file_browser = base_windows.File_Dialogue()
        _selection_item = _file_browser.getOpenFileName(
            parent=self,
            caption=("Select Scene"),
            dir="/home",
            # filter=("*.ma, *.mb, *.fbx")
        )
        _selected_file = _selection_item[0]
        logger.debug(f'File selected {_selected_file}')
        self.filepath = _selected_file
        self.FileSelected.emit(_selected_file)


class Folder_Selection_Line_Edit(base_layouts.Horizontal_Layout):
    FileSelected = QtCore.Signal(str)
    textEdited = QtCore.Signal(str)

    def __init__(self, directory,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_edit = None
        self.build_widget(directory)

    @property
    def directory(self):
        return self.line_edit.text()

    def build_widget(self, filepath):
        self.line_edit = self.build_lineedit(filepath)
        self.button = self.build_button()

        self.addWidget(self.line_edit)
        self.addWidget(self.button, alignment=constants.align_right)


    def build_lineedit(self, filepath):
        filepath = filepath if os.path.exists(filepath) else ""
        _line_edit = base_widgets.Line_Edit(text=filepath)
        _line_edit.textEdited.connect(self.textEdited.emit)
        self.FileSelected.connect(_line_edit.setText)
        return _line_edit

    def build_button(self):
        _button = base_widgets.Tool_Button()
        _button.setIcon(icons.open_file)
        _button.clicked.connect(self.open_file_dialogue)
        return _button

    def open_file_dialogue(self):
        _file_browser = base_windows.File_Dialogue()
        _selection_item = _file_browser.getExistingDirectory(
            parent=self,
            caption=("Select Export Directory"),
            dir="/home"
        )
        _selected_file = _selection_item
        logger.debug(f'File selected {_selected_file}')
        self.filepath = _selected_file
        self.FileSelected.emit(_selected_file)

class TwoDimensionalFloat(base_layouts.Horizontal_Layout):
    valueChanged = QtCore.Signal(list)

    def __init__(self, x_val, y_val, *args, **kwargs):
        super().__init__(spacing=5, *args, **kwargs)

        self.x_line = FloatLineEdit(value=x_val)
        self.x_line.textEdited.connect(self.emit_value_changed)
        self.y_line = FloatLineEdit(value=y_val)
        self.y_line.textEdited.connect(self.emit_value_changed)

        self.addWidget(self.x_line)
        self.addWidget(self.y_line)

    @property
    def value(self):
        return [self.x_value, self.y_value]

    @property
    def x_value(self):
        return self.x_line.value()

    def set_x_value(self, value):
        self.x_line.setValue(value)

    def emit_value_changed(self, *args):
        self.valueChanged.emit([self.x_value, self.y_value])

    @property
    def y_value(self):
        return self.y_line.value()

    def set_y_value(self, value):
        self.y_line.setValue(value)
