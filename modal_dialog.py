import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from pyqt_interface_elements import base_widgets, icons, base_windows, line_edits, base_layouts, constants
from PySide2 import QtCore, QtWidgets


class ChooseFilePath(base_windows.Dialog):

    def __init__(self):
        super().__init__()

        self.file_path_button = line_edits.Folder_Selection_Line_Edit()

class ConfirmDialogue(base_windows.Dialog):
    confirmed = QtCore.Signal()

    def __init__(self, display_text, cancel_text="Cancel", confirm_text="Confirm", parent=None):
        super().__init__(parent=parent)

        _label = base_widgets.Label(text=display_text)

        _cancel = base_widgets.Button(text=cancel_text)
        _cancel.clicked.connect(self._cancel)
        _confirm = base_widgets.Button(text=confirm_text)
        _confirm.clicked.connect(self._confirm)

        _buttons = base_layouts.HorizontalLayout()
        _buttons.addWidgets([_cancel, _confirm])

        _layout = QtWidgets.QVBoxLayout()
        self.setLayout(_layout)

        _layout.addWidget(_label, alignment=constants.align_center, stretch=1)
        _layout.addWidget(_buttons, alignment=constants.align_bottom | constants.align_right)

    def _confirm(self):
        """
        Emits the confirmed signal and closes the window

        """
        self.confirmed.emit()
        self.close()


    def _cancel(self):
        """
        Closes the window

        """
        self.close()


