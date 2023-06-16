
from PySide2 import QtCore, QtWidgets, QtGui
from interface_elements import constants


class Layout(QtWidgets.QWidget):

    def __init__(self, layout_orientation, margins=[0, 0, 0, 0], spacing=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = QtWidgets.QVBoxLayout() if layout_orientation == constants.vertical else QtWidgets.QHBoxLayout()

        self.layout.setContentsMargins(
            margins[0],
            margins[1],
            margins[2],
            margins[3]
        ) if isinstance(
            margins,
            list
        ) else self.layout.setContentsMargins(
            margins,
            margins,
            margins,
            margins
        )
        self.layout.setSpacing(spacing)

        self.children = []

        self.setLayout(self.layout)

    @property
    def layout(self):
        return self._layout

    def addWidget(self, widget, *args, **kwargs):
        self.layout.addWidget(widget, *args, **kwargs)
        self.children.append(widget)

    def addWidgets(self, widgets, *args, **kwargs):
        [self.addWidget(_widget, *args, **kwargs) for _widget in widgets]

    def clear_layout(self):
        for _child in self.children:
            self.disown_child(_child)

    def disown_child(self, child_widget):
        child_widget.deleteLater()
        _index = self.children.index(child_widget)
        self.children.pop(_index)


class Vertical_Layout(Layout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0, *args, **kwargs):
        super().__init__(layout_orientation=constants.vertical, margins=margins, spacing=spacing, *args, **kwargs)


class Horizontal_Layout(Layout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0, *args, **kwargs):
        super().__init__(layout_orientation=constants.horizontal, margins=margins, spacing=spacing, *args, **kwargs)


