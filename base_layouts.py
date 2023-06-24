
from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import constants


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

    def paintEvent(self, event):
        self.setAutoFillBackground(True)

        super().paintEvent(event)


    @property
    def layout(self):
        return self._layout

    def addStretch(self, stretch):
        self.layout.addStretch(stretch)

    def addWidget(self, widget, *args, **kwargs):
        self.layout.addWidget(widget, *args, **kwargs)
        self.children.append(widget)

    def addWidgets(self, widgets, *args, **kwargs):
        [self.addWidget(_widget, *args, **kwargs) for _widget in widgets]

    def insertWidget(self, index, widget):
        self.layout.insertWidget(index, widget)
        self.children.append(widget)

    def addSpacerItem(self, spaceritem):
        self.layout.addSpacerItem(spaceritem)

    def insertSpacerItem(self, index, spaceritem):
        self.layout.insertSpacerItem(index, spaceritem)

    def clearAndAddWidget(self, widget, *args, **kwargs):
        self.clear_layout()
        self.layout.addWidget(widget, *args, **kwargs)
        self.children.append(widget)

    def clearAndAddWidgets(self, widgets, *args, **kwargs):
        self.clear_layout()
        self.addWidgets(widgets, *args, **kwargs)

    def clear_layout(self):
        if len(self.children) > 0:
            for _child in self.children:
                self.disown_child(_child)

            self.children = []

    def disown_child(self, child_widget):
        child_widget.setParent(None)
        del child_widget
        # _index = self.children.index(child_widget)
        # self.children.pop(_index)


class Vertical_Layout(Layout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(layout_orientation=constants.vertical, margins=margins, spacing=spacing)


class Horizontal_Layout(Layout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(layout_orientation=constants.horizontal, margins=margins, spacing=spacing)


class Splitter(QtWidgets.QSplitter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TabWidget(QtWidgets.QTabWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _window = TabWidget()
        _window.addTab(QtWidgets.QPushButton("but"), "test")

        _m = Splitter()
        _m.addWidget(_window)
        _m.show()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())
