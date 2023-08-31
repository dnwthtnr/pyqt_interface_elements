import logging
import os.path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import file_management
from functools import partial
from pyqt_interface_elements import base_widgets, icons, base_windows, line_edits, base_layouts, constants, proceadural_displays
from PySide2 import QtCore, QtWidgets, QtGui


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
    fileCreated = QtCore.Signal(str)
    
    def __init__(self):
        super().__init__()
        _layout = QtWidgets.QVBoxLayout()
        self.setLayout(_layout)

        self._file_browser = base_windows.File_Dialogue()
        self._file_browser.fileSelected.connect(self._file_selected)

        self._selected_file = None

        self._toolbar = self._build_toolbar()

        self.addWidget(self._file_browser, stretch=1)
        self.addWidget(self._toolbar)

        self.resize(900, 700)

    def addWidget(self, widget, *args, **kwargs):
        self.layout().addWidget(widget, *args, **kwargs)

    def addToolbarWidget(self, widget, *args, **kwargs):
        self._toolbar.addWidget(widget, *args, **kwargs)

    def setupAddFileButton(self, text='New File', title_text="New File:", icon=QtGui.QIcon(), file_extensions=['.json']):
        """
        Creates a button that when clicked will create a new file
        Parameters
        ----------
        text
        icon

        Returns
        -------

        """
        _button = line_edits.BuildFileName(extensions=file_extensions, title_text=title_text)
        _button.fileNameChosen.connect(self.createFile)
        self.addToolbarWidget(_button)

    @QtCore.Slot('createFile')
    def createFile(self, fileName):
        _qdirectory = self._file_browser.directory()
        _path = _qdirectory.path()
        _new_path = file_management.generate_unique_file_name(_path, fileName)

        file_management.create_file(_new_path)

        _qdirectory.refresh()

    def _build_toolbar(self):
        _widget = base_layouts.HorizontalLayout(margins=[12, 0, 12, 0])
        return _widget

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
    _view.setupAddFileButton()

    # _win = base_windows.Main_Window()
    # _win.setCentralWidget(_view)
    _view.show()

    sys.exit(_app.exec_())