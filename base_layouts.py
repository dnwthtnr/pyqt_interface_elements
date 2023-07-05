from functools import partial
from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import constants, buttons, icons


class Layout(QtWidgets.QWidget):

    def __init__(self, layout_orientation, margins=[0, 0, 0, 0], spacing=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = QtWidgets.QVBoxLayout() if layout_orientation == constants.vertical else QtWidgets.QHBoxLayout()

        self.stretch = False

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
        self.stretch = True

    def addWidget(self, widget, *args, **kwargs):
        if self.stretch is True:
            self.insertWidget(0, widget)
            self.children.append(widget)
            return
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

    def childCount(self):
        return len(self.children)

    def disown_child(self, child_widget):
        child_widget.setParent(None)
        del child_widget
        # _index = self.children.index(child_widget)
        # self.children.pop(_index)


class VerticalLayout(Layout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(layout_orientation=constants.vertical, margins=margins, spacing=spacing)


class HorizontalLayout(Layout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(layout_orientation=constants.horizontal, margins=margins, spacing=spacing)


class ScrollArea(QtWidgets.QScrollArea):

    # def __getattr__(self, item):
    #
    #     if hasattr(self.layout, item):
    #         # _attr = getattr(self.layout, item)
    #         return getattr(self.layout, item)
    #     else:
    #         raise AttributeError(f'Class {self.__class__.__name__} does not have attribute: {item}')

    def __init__(self, layout_orientation, margins=[0, 0, 0, 0], spacing=0, *args, **kwargs):
        super().__init__()
        self._layout = Layout(
            layout_orientation=layout_orientation,
            margins=margins,
            spacing=spacing,
            *args,
            **kwargs
        )

        self.setWidget(self.layout)
        self.setWidgetResizable(True)

    @property
    def layout(self):
        return self._layout

    def addStretch(self, stretch):
        self.layout.addStretch(stretch)

    def addWidget(self, widget, *args, **kwargs):
        self.layout.addWidget(widget, *args, **kwargs)

    def addWidgets(self, widgets, *args, **kwargs):
        self.layout.addWidgets(widgets, *args, **kwargs)

    def insertWidget(self, index, widget):
        self.layout.insertWidget(index, widget)

    def addSpacerItem(self, spaceritem):
        self.layout.addSpacerItem(spaceritem)

    def insertSpacerItem(self, index, spaceritem):
        self.layout.insertSpacerItem(index, spaceritem)

    def clearAndAddWidget(self, widget, *args, **kwargs):
        self.layout.clearAndAddWidget(widget, *args, **kwargs)

    def clearAndAddWidgets(self, widgets, *args, **kwargs):
        self.layout.clearAndAddWidgets( widgets, *args, **kwargs)

    def clear_layout(self):
        self.layout.clear_layout()

    def childCount(self):
        self.layout.childCount()

    def disown_child(self, child_widget):
        self.layout.disown_child(child_widget)


class VerticalScrollArea(ScrollArea):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(layout_orientation=constants.vertical, margins=margins, spacing=spacing)


class HorizontalScrollArea(ScrollArea):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(layout_orientation=constants.horizontal, margins=margins, spacing=spacing)


class Splitter(QtWidgets.QSplitter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TabWidget(QtWidgets.QTabWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ExpandWhenClicked(HorizontalLayout):

    def __init__(self, margins=[0, 0, 0, 0], spacing=0, *args, **kwargs):
        super().__init__(margins=margins, spacing=spacing, *args, **kwargs)

        self.dropdown = self.build_dropdown_button()

        self.collapsed_layout = self.build_collapsed()
        self.expanded_layout = self.build_expanded(margins, spacing)



        _layouts = VerticalLayout()
        _layouts.addWidget(self.collapsed_layout, alignment=constants.align_top)
        _layouts.addWidget(self.expanded_layout)

        _bar_layout = HorizontalLayout()
        _bar_layout.addWidget(self.dropdown, alignment=constants.align_left | constants.align_top)
        _bar_layout.addWidget(_layouts)


        self.addWidget(_bar_layout)

    def build_dropdown_button(self):
        _dropdown = buttons.ToggleIconButton(enabled_icon=icons.down_arrow, disabled_icon=icons.up_arrow)
        _dropdown.setStyleSheet("background-color: transparent; border: none;")
        _dropdown.enabled.connect(partial(self.setExpandedState, True))
        _dropdown.disabled.connect(partial(self.setExpandedState, False))
        return _dropdown

    def build_collapsed(self):

        _layout = HorizontalLayout()

        return _layout

    def build_expanded(self, margins, spacing):
        _layout = VerticalLayout(margins=margins, spacing=spacing)
        _layout.hide()
        return _layout

    def set_collapsed_stylesheet(self, stylesheet):
        self.collapsed_layout.setStyleSheet(stylesheet)
        self.dropdown.setStyleSheet(stylesheet)

    def set_expanded_stylesheet(self, stylesheet):
        self.expanded_layout.setStyleSheet(stylesheet)

    def addCollapsedWidget(self, widget, *args, **kwargs):
        self.collapsed_layout.addWidget(widget, *args, **kwargs)

    def addExpandedWidget(self, widget, *args, **kwargs):
        self.expanded_layout.addWidget(widget, *args, **kwargs)

    def setExpandedState(self, expanded):
        if expanded is True:
            self.expanded_layout.show()
        else:
            self.expanded_layout.hide()

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
