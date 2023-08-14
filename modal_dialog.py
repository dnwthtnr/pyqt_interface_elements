import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from pyqt_interface_elements import base_widgets, icons, base_windows, line_edits, base_layouts
from PySide2 import QtCore


class ChooseFilePath(base_windows.Dialog):

    def __init__(self):
        super().__init__()

        self.file_path_button = line_edits.Folder_Selection_Line_Edit()

class ConfirmDialogue(base_windows.Dialog):
    confirm = QtCore.Signal()

    def __init__(self, display_text):
        super().__init__()

        _label = base_widgets.Label(text=display_text)

        _cancel = base_widgets.Button(text="Cancel")
        _confirm = base_widgets.Button(text="Confirm")

        _buttons = base_layouts.HorizontalLayout()
        _buttons.addWidgets([_cancel, _confirm])

        _layout = base_layouts.VerticalLayout()
        self.setLayout(_layout)

        _layout.addWidget(_label)


