from pyqt_interface_elements import base_widgets
from PySide2 import QtCore


class ToggleIconButton(base_widgets.Tool_Button):
    enabled = QtCore.Signal()
    disabled = QtCore.Signal()


    def __init__(self, enabled_icon, disabled_icon):
        super().__init__()
        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        print(self.enabled_icon, self.disabled_icon)

        self.setIcon(self.enabled_icon)
        self._enabled = True
        self.clicked.connect(self.toggleIcon)

    @property
    def enabledState(self):
        return self._enabled

    @enabledState.setter
    def enabledState(self, value):
        self._enabled = value

    def toggleIcon(self):
        print('toggle', self.enabledState)
        if self.enabledState is True:
            self.setIconState(False)
        else:
            self.setIconState(True)

    def setIconState(self, enabled):
        print('state', enabled)
        if enabled is False:
            self.setIcon(self.disabled_icon)
            self.enabledState = False
            self.disabled.emit()
        else:
            self.setIcon(self.enabled_icon)
            self.enabledState = True
            self.enabled.emit()



