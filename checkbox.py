from pyqt_interface_elements import base_layouts, base_widgets, line_edits, buttons, icons
from PySide2 import QtWidgets

#TODO: finish range selection


class TwoDimensionalCheckBox(base_layouts.Horizontal_Layout):

    def __init__(self, range):
        super().__init__()

        self.checkbox = buttons.ToggleIconButton(enabled_icon=icons.up_arrow, disabled_icon=icons.down_arrow)
        self.two_dimensional_editor = line_edits.TwoDimensionalFloat(x_val=range[0], y_val=range[1])

        self.addWidget(self.checkbox)
        self.addWidget(self.two_dimensional_editor)



class CustomFromRangesCheckbox(base_layouts.Vertical_Layout):

    def __init__(self, ranges_list, row_max=4):
        super().__init__()

        _row = base_layouts.Horizontal_Layout()
        for _range_list in ranges_list:
            _x_val = _range_list[0]
            _y_val = _range_list[1]
            # _range_editor = line_edits.TwoDimensionalFloat(_x_val, _y_val)
            _range_editor = TwoDimensionalCheckBox(range=_range_list)
            _row.addWidget(_range_editor)
            if _row.childCount() == 4:
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
