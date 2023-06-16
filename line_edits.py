
from pyqt_interface_elements import constants, base_layouts, base_widgets, base_windows, icons
from PySide2 import QtCore, QtWidgets, QtGui
from functools import partial
import os


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class File_Selection_Line_Edit(base_layouts.Horizontal_Layout):
    FileSelected = QtCore.Signal(str)

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

