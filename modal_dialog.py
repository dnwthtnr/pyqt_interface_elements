import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from pyqt_interface_elements import base_widgets, icons, base_windows
from PySide2 import QtCore


class ChooseFilePath(base_windows.Dialog):

    def __init__(self):
        super().__init__()


