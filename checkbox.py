import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from pyqt_interface_elements import base_layouts, base_widgets, line_edits, buttons, icons
from PySide2 import QtWidgets, QtCore
from functools import partial

#TODO: finish range selection


class Checkbox(buttons.ToggleIconButton):
    checked = QtCore.Signal()
    unchecked = QtCore.Signal()

    def __init__(self):
        super().__init__(enabled_icon=icons.checkbox_checked, disabled_icon=icons.checkbox_unchecked)
        self.enabled.connect(self.checked.emit)
        self.disabled.connect(self.unchecked.emit)


class CheckBoxLayout(base_layouts.Horizontal_Layout):
    checked = QtCore.Signal()
    unchecked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.checkbox = Checkbox()
        self.checkbox.checked.connect(self.checked.emit)
        self.checkbox.unchecked.connect(self.unchecked.emit)
        self.addWidget(self.checkbox)

    def setChecked(self, checked):
        self.checkbox.setIconState(checked)


class TwoDimensionalCheckBox(CheckBoxLayout):

    def __init__(self, range):
        super().__init__()
        self.two_dimensional_editor = line_edits.TwoDimensionalFloat(x_val=range[0], y_val=range[1])
        self.addWidget(self.two_dimensional_editor)


class CheckboxManager(QtCore.QObject):

    def __init__(self, allowed_checked_limit=5):
        super().__init__()
        self._checked_limit = allowed_checked_limit

        self.checkboxes = {}
        self.checked = []

    def checkedLimit(self):
        return self._checked_limit

    def checkedCount(self):
        return len(self.checked)

    def currentlyChecked(self):
        """
        The currently checked checkboxes

        Returns
        -------

        """
        return self.checked

    def addCheckBox(self, checkbox_instance, checkbox_checked_signal, checkbox_unchecked_signal, uncheck_checkbox_callable):
        """
        Adds checkbox
        Parameters
        ----------
        checkbox_instance
        checkbox_checked_signal
        uncheck_checkbox_callable

        Returns
        -------

        """
        checkbox_checked_signal.connect(partial(self.checkboxChecked, checkbox_instance))
        checkbox_unchecked_signal.connect(partial(self.checkboxUnchecked, checkbox_instance))
        self.checkboxes[checkbox_instance] = uncheck_checkbox_callable

    @QtCore.Slot()
    def checkboxChecked(self, checkbox):
        self.checked.append(checkbox)
        if self.checkedCount() > self.checkedLimit():
            _checkbox_to_uncheck = self.checked[0]

            _uncheck_checkbox_callable = self.checkboxes[_checkbox_to_uncheck]
            _uncheck_checkbox_callable()

            logger.debug(f'Unchecked checkbox: {_checkbox_to_uncheck}')

    @QtCore.Slot()
    def checkboxUnchecked(self, checkbox):
        _checkbox_index = self.checked.index(checkbox)
        self.checked.pop(_checkbox_index)


class CustomFromRangesCheckbox(base_layouts.Vertical_Layout):

    def __init__(self, ranges_list, row_max=6):
        super().__init__()

        self.editors = []
        checkbox_manager = CheckboxManager()

        _row = base_layouts.Horizontal_Layout()
        for _range_list in ranges_list:
            _range_editor = TwoDimensionalCheckBox(range=_range_list)
            checkbox_manager.addCheckBox(
                checkbox_instance=_range_editor,
                checkbox_unchecked_signal=_range_editor.unchecked,
                checkbox_checked_signal=_range_editor.checked,
                uncheck_checkbox_callable=partial(_range_editor.setChecked, False)
            )
            # _range_editor.checked.connect(partial(checkbox_manager.checkboxChecked, _range_editor))
            # _range_editor.unchecked.connect(partial(checkbox_manager.checkboxUnchecked, _range_editor))

            _row.addWidget(_range_editor)
            self.editors.append(_range_editor)
            if _row.childCount() == row_max:
                self.addWidget(_row)
                _row = base_layouts.Horizontal_Layout()
        self.addWidget(_row)

if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _window = CustomFromRangesCheckbox(ranges_list=[
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200],
            [10, 200]
        ])
        _window.show()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())
