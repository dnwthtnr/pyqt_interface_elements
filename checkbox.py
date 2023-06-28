from pyqt_interface_elements import base_layouts, base_widgets, line_edits

#TODO: finish range selection

class CustomFromRangesCheckbox(base_layouts.Vertical_Layout):

    def __init__(self, ranges_list, row_max=4):
        super().__init__()

        _row = base_layouts.Horizontal_Layout()
        for _range_list in ranges_list:
            _x_val = _range_list[0]
            _y_val = _range_list[1]
            _range_editor = line_edits.TwoDimensionalFloat(_x_val, _y_val)
            _row.addWidget(_range_editor)
            if _row.childCount() == 4:
                self.addWidget(_row)
                _row = base_layouts.Horizontal_Layout()
