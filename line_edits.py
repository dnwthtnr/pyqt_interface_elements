
from pyqt_interface_elements import constants, base_layouts, base_widgets, base_windows, icons, buttons, modal_dialog
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


class File_Selection_Line_Edit(base_layouts.HorizontalLayout):
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
        _line_edit.setReadOnly(True)
        _line_edit.textEdited.connect(self.textEdited.emit)
        self.FileSelected.connect(_line_edit.setText)
        return _line_edit

    def set_display_path(self, filepath):
        if os.path.exists(filepath) is False:
            return

        self.line_edit.setText(filepath)

    def build_button(self):
        _button = base_widgets.Tool_Button()
        _button.setStyleSheet("border: none;")
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

        if os.path.exists(_selected_file) is False:
            return

        self.filepath = _selected_file
        self.FileSelected.emit(_selected_file)


class Folder_Selection_Line_Edit(base_layouts.HorizontalLayout):
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
        _button.setStyleSheet("border: none;")
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

    def set_directory(self, directory):
        self.line_edit.setText(directory)


class TwoDimensionalFloat(base_layouts.HorizontalLayout):
    valueChanged = QtCore.Signal(list)

    def __init__(self, x_val, y_val, seperator="-", *args, **kwargs):
        super().__init__(spacing=5, *args, **kwargs)

        self.x_line = FloatLineEdit(value=x_val)
        self.x_line.setAlignment(constants.align_left)
        self.x_line.textEdited.connect(self.emit_value_changed)

        self.y_line = FloatLineEdit(value=y_val)
        self.y_line.setAlignment(constants.align_left)
        self.y_line.textEdited.connect(self.emit_value_changed)

        self.seperator = base_widgets.Label(text=seperator)

        self.addWidget(self.x_line)
        self.addWidget(self.seperator)
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


class ListToolTipDisplay(base_widgets.Line_Edit):
    seperator = " :: "

    def __init__(self, _list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setList(_list)
        self.setAlignment(constants.align_left)
        self.setReadOnly(True)

    def list(self):
        _tooltip_text = self.toolTip()
        _list = _tooltip_text.split(self.seperator)
        return _list

    def setList(self, _list):
        self.setText(f"{len(_list)} Children")
        # self.setToolTip("".join(_list))


class LabelEditor(base_widgets.Label):

    def __init__(self, update_text=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_text = update_text
        self._line_edit = base_widgets.Line_Edit()

    def enter_editing(self):

        # _rect_local = self.rect()
        #
        # self._line_edit.setGeometry(self.rect())
        #
        # self._line_edit.move(self.mapToGlobal(self.pos()))

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._line_edit.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self._line_edit.setWindowFlag(QtCore.Qt.Tool, True)
        self._line_edit.setText(self.text())
        self._line_edit.show()
        return

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._line_edit.setGeometry(self.rect())
        self._line_edit.move(self.mapToGlobal(self.pos()))

    def exit_editing(self):
        self._line_edit.hide()
        if self.update_text is True:
            self.setText(self._line_edit.text())
            return

        return self._line_edit.text()


class NameEditor(base_layouts.HorizontalLayout):
    textEdited = QtCore.Signal(str)

    def __init__(self, name):
        super().__init__()
        self._label = self._build_label(name)
        self._button = self._build_button()

        self.addWidget(self._label, stretch=1)
        self.addWidget(self._button)


    def text(self):
        return self._label.text()

    def setText(self, text):
        self._label.setText(text)


    def _build_label(self, name):
        _widget = LabelEditor(text=name, update_text=False)
        return _widget

    def _build_button(self):
        _widget = buttons.ToggleIconButton(enabled_icon=icons.open_file, disabled_icon=icons.checkbox_checked)
        _widget.disabled.connect(self.exit_edit_mode)
        _widget.enabled.connect(self.enter_edit_mode)
        return _widget

    def enter_edit_mode(self):
        self._label.enter_editing()
        return

    def exit_edit_mode(self):
        _new_name = self._label.exit_editing()
        _old_name = self._label.text()
        if _new_name == _old_name:
            return

        self._name_change_confirmation(_old_name, _new_name)


    def _name_change_confirmation(self, old_name, new_name):
        self._confirmation_dialogue = modal_dialog.ConfirmDialogue(
            display_text=f'Are you sure you want to rename {old_name} to {new_name}?'
        )
        self._confirmation_dialogue.confirmed.connect(partial(self.textEdited.emit, new_name))

        self._confirmation_dialogue.show()


if __name__ == "__main__":
    from pyqt_interface_elements import base_windows
    import sys
    from animation_exporter.utility_resources import settings
    from PySide2 import QtWidgets


    _app = QtWidgets.QApplication(sys.argv)
    _view = NameEditor("name")

    # _win = base_windows.Main_Window()
    # _win.setCentralWidget(_view)
    _view.show()

    sys.exit(_app.exec_())
