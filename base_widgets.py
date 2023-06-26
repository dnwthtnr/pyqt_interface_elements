
from PySide2 import QtCore, QtWidgets, QtGui

class Line_Edit(QtWidgets.QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Tool_Button(QtWidgets.QToolButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Label(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TextEdit(QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Spacer(QtWidgets.QSpacerItem):

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)


class ComboBox(QtWidgets.QComboBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
