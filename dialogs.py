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

class FileDialog(base_windows.Dialog):
    
    def __init__(self):
        super().__init__()

        self._file_browser = base_windows.File_Dialogue()
        self._file_browser.fileSelected.connect(self._file_selected)

        self._selected_file = None

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self._file_browser)
        self.setLayout(self.layout)
        self.resize(900, 700)

    def addWidget(self, widget, *args, **kwargs):
        self.layout.addWidget(widget, *args, **kwargs)


    def _file_selected(self, file):
        print(file)
        self._selected_file = file

        self.close()

if __name__ == "__main__":
    from pyqt_interface_elements import base_windows
    import sys
    from animation_exporter.utility_resources import settings
    from PySide2 import QtWidgets

    _app = QtWidgets.QApplication(sys.argv)
    _view = FileDialog()
    _view.addWidget(base_widgets.Button(text='Add New Queue'), alignment=constants.align_right)

    # _win = base_windows.Main_Window()
    # _win.setCentralWidget(_view)
    _view.show()

    sys.exit(_app.exec_())