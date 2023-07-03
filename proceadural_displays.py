import os.path
from PySide2 import QtCore
from pyqt_interface_elements import (
    base_layouts,
    base_windows,
    constants,
    base_widgets,
    icons,
    line_edits,
    text_edit,
    labels,
    checkbox
)


class AbstractAttributeEntry(base_layouts.Horizontal_Layout):
    valueEdited = QtCore.Signal(object)

    def __init__(self, attribute_name, attribute_value):
        super().__init__(spacing=15)
        self.title_label = self.build_attribute_name_label(attribute_name)

        self.attribute_editor_widget = self.attribute_editor(attribute_value)

        self.addWidget(self.title_label, alignment=constants.align_left)
        self.addWidget(self.attribute_editor_widget)

    @property
    def attribute_name(self):
        return self.title_label.text()

    @property
    def attribute_value(self):
        return self.attribute_editor_value(self.attribute_editor_widget)

    def set_title_fixed_width(self, width):
        self.title_label.setFixedWidth(width)

    def attribute_editor(self, attribute_value):
        raise NotImplementedError(f"You must implement {self.__class__.__name__}.attribute_editor()")

    def attribute_editor_value(self, attribute_editor):
        raise NotImplementedError(f"You must implement {self.__class__.__name__}.attribute_editor_value()")

    def build_attribute_name_label(self, name):
        _label = base_widgets.Label(text=name)
        _label.setAlignment(constants.align_right)
        return _label

    def identifier(self, value):
        raise NotImplementedError(f"You must implement {self.__class__.__name__}.identifier()")

    def setReadOnly(self, enabled):
        _attr = getattr(self.attribute_editor_widget, "setReadOnly", None)
        if not callable(_attr):
            return
        self.attribute_editor_widget.setReadOnly(enabled)

class LineEditAttributeEditor(AbstractAttributeEntry):
    IDENTIFIER = str

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = base_widgets.Line_Edit(text=attribute_value)
        _widget.textEdited.connect(self.valueEdited.emit)
        return _widget

    def attribute_editor_value(self, attribute_editor):
        return attribute_editor.text()

    def identifier(self, value):
        if isinstance(value, str):
            return True
        return False

class FilepathDisplayAttributeEditor(AbstractAttributeEntry):

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = line_edits.File_Selection_Line_Edit(filepath=attribute_value)
        return _widget

    def attribute_editor_value(self, attribute_editor):
        return attribute_editor.filepath

    def identifier(self, value):
        if not isinstance(value, str):
            return False
        if not os.path.exists(value):
            return False
        if not os.path.isfile(value):
            return False
        return True

class ChooseDirectoryAttributeEditor(AbstractAttributeEntry):

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = line_edits.Folder_Selection_Line_Edit(directory=attribute_value)
        _widget.textEdited.connect(self.valueEdited.emit)
        return _widget

    def attribute_editor_value(self, attribute_editor):
        return attribute_editor.directory

    def identifier(self, value):
        if not isinstance(value, str):
            return False
        if not os.path.exists(value):
            return False
        if not os.path.isdir(value):
            return False
        return True

class LargeListAttributeEditor(AbstractAttributeEntry):

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = text_edit.LargeListDisplay(_list=attribute_value)
        return _widget

    def attribute_editor_value(self, attribute_editor):
        return attribute_editor.list()

    def identifier(self, value):
        if not isinstance(value, list):
            return False
        if len(value) < 0:
            return False

        return True

class LargeListTooltipAttributeEditor(AbstractAttributeEntry):

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = line_edits.ListToolTipDisplay(_list=attribute_value)
        return _widget

    def attribute_editor_value(self, attribute_editor):
        return attribute_editor.list()

    def identifier(self, value):
        if not isinstance(value, list):
            return False
        if len(value) < 0:
            return False

        # check if all contents are lists
        _contents_list = [isinstance(_item, list) for _item in value]
        if True in _contents_list:
            return False

        return True

class TwoDimentionalLineEditAttributeEditor(AbstractAttributeEntry):

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = line_edits.TwoDimensionalFloat(x_val=attribute_value[0], y_val=attribute_value[1])
        return _widget

    def attribute_editor_value(self, attribute_editor):
        return [attribute_editor.x_value, attribute_editor.y_value]

    def identifier(self, value):
        if not isinstance(value, list):
            return False
        elif not len(value) == 2:
            return False
        elif [type(value[0]), type(value[1])] != [float, float]:
            return False
        else:
            return True

class RangeCheckboxArrayAttributeEditor(AbstractAttributeEntry):

    def __int__(self, attribute_name, attribute_value):
        super().__init__(attribute_name, attribute_value)

    def attribute_editor(self, attribute_value):
        _widget = checkbox.RangeCheckboxArray(ranges_list=attribute_value)
        return _widget

    def attribute_editor_value(self, attribute_editor):
        """

        Parameters
        ----------
        attribute_editor

        Returns
        -------
        list[list]

        """
        return attribute_editor.checked_ranges()

    def identifier(self, value):
        if not isinstance(value, list):
            return False

        # check if all contents are lists
        _contents_list = [isinstance(_item, list) for _item in value]
        if False in _contents_list:
            return False

        # check if all lists are of length 2
        _contents_all_ranges = [len(_item) == 2 for _item in value]
        if False in _contents_all_ranges:
            return False

        # check if all lists hold 2 ints
        for _item in value:
            _item_type_pair = [type(_item[0]), type(_item[1])]
            if _item_type_pair != [float, float] and _item_type_pair != [int, int]:
                return False

        return True


class AbstractEntryHolder(base_layouts.Vertical_Layout):

    def __init__(self, attribute_dictionary, attribute_mapping_dictionary, map_by_type=True, attribute_title_width=150, margins=[0, 0, 0, 0], spacing=0):
        super().__init__(margins, spacing)
        self.attribute_entries = []
        self._build(attribute_dictionary, attribute_mapping_dictionary, map_by_type, attribute_title_width)

    def _build(self, attribute_dictionary, attribute_mapping_dictionary, map_by_type, attribute_title_width):
        for _attribute_name, _attribute_value in attribute_dictionary.items():
            _attribute_entry = self.create_attribute_entry(
                _attribute_name,
                _attribute_value,
                attribute_mapping_dictionary,
                map_by_type
            )
            if _attribute_entry is None:
                continue
            _attribute_entry.set_title_fixed_width(attribute_title_width)
            self.addWidget(_attribute_entry)
            self.attribute_entries.append(_attribute_entry)
        self.addStretch(1)

    def attribute_dictionary(self):
        _attribute_dictionary = {}
        for _entry in self.attribute_entries:
            _attribute_dictionary[_entry.attribute_name] = _entry.attribute_value

        return _attribute_dictionary



    def create_attribute_entry(self, attribute_name, attribute_value, attribute_mapping_dictionary, map_by_type):
        if map_by_type is True:
            return self.create_attribute_entry_by_type(attribute_name, attribute_value, attribute_mapping_dictionary)
        raise NotImplementedError(
            f"You must implement {self.__class__.__name__}.map_attribute() when not automapping by type.")

    def create_attribute_entry_by_type(self, attribute_name, attribute_value, attribute_mapping_dictionary):
        _entry = attribute_mapping_dictionary[type(attribute_value)]
        return _entry(attribute_name, attribute_value)


if __name__ == "__main__":
    class attr(AbstractAttributeEntry):

        def __init__(self):
            super().__init__(attr)
