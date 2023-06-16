from PySide2 import QtCore, QtWidgets, QtGui

# TODO stuff is not working


"""
This file holds a data mode class specialized for the organization of catalog content data
"""
from PySide2 import QtCore



class CatalogContentTableModel(QtCore.QAbstractTableModel):
    CatalogEmpty = QtCore.Signal()

    def __init__(self, catalog_content_dict):
        """
        This class models the given catalog content data for use to be displayed.

        Parameters
        ----------
        catalog_content_dict : dict
            The catalog content data to organize for displaying
        """
        self.empty_catalog = {
                "No Catalog Selected": {
                    "Name": "No projects are present in the catalog"
                }
            }
        super().__init__()
        if catalog_content_dict == {}:
            self.catalog_content_dict = self.empty_catalog
            self._empty = True
        else:
            self._empty = False
            self.catalog_content_dict = catalog_content_dict

        self.headers = ["Project Name", "Asset Group", "Local Check-in Status", "Last Modified"]

    def finish_initialization(self):
        """
        Emits empty signal if the dictionary has nothing in it

        """
        if self.catalog_content_dict == self.empty_catalog:
            self.CatalogEmpty.emit()

    def key_for_row(self, row):
        """
        For the given row number will return the key
        that represents it in the data dictionary

        Parameters
        ----------
        row : int
            The row to get

        Returns
        -------
        str
            The key representing the given row

        """
        data_keys = list(self.catalog_content_dict.keys())
        return data_keys[row]

    def row_for_key(self, key):
        """
        Gets the row that the given key would take up

        Parameters
        ----------
        key : str
            The key to get the row value for (project name)

        Returns
        -------
        int
            The row number

        """
        _data_keys = list(self.catalog_content_dict.keys())
        for _row in range(0, self.rowCount()):
            if self.key_for_row(_row) == key:
                return _row

    def rowCount(self, parent=None, *args, **kwargs):
        """
        The amount of rows in the model

        Parameters
        ----------
        parent : QModelIndex
            Parent index
        args :
        kwargs :

        Returns
        -------
        int
            The amount of rows

        """
        return len(list(self.catalog_content_dict.keys()))

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Column amount is based on the amount of data given in the dict for each project

        Parameters
        ----------
        parent : QtCore.QModelIndex
            The parent model index -- not applicable in a table model
        args :
        kwargs :

        Returns
        -------
        int
            The amount of columns

        """
        _key_for_first_row = self.key_for_row(0)
        _dict_for_first_row = self.catalog_content_dict[_key_for_first_row]
        return len(_dict_for_first_row)

    def data(self, index, role=None):
        """
        Returns the data for the given index and role

        Parameters
        ----------
        index : QtCore.QModelIndex
            The index to get data for
        role : QtCore.Qt.Role
            The role to get data for

        Returns
        -------
        object
            The data for the given row and role

        """
        if role == QtCore.Qt.DisplayRole:
            _row = index.row()
            _column = index.column()

            _key_for_row = self.key_for_row(_row)       # project name -- is key for the main contents dict
            _dict_for_row = self.catalog_content_dict[_key_for_row]     # the dictionary for that given project
            _dict_key_list = list(_dict_for_row.values())       # list of that dicts values

            return _dict_key_list[_column]

    def headerData(self, section, orientation, role=None):
        """
        Returns the header data for the given index and role

        Parameters
        ----------
        section : int
            The index to get header data for.
        orientation : QtCore.Qt.Orientation
            The orientation of the header to get data for.
        role : QtCore.Qt.Role
            The role to get header data for.

        Returns
        -------
        object
            The header data for the given header index and row

        """
        if role != QtCore.Qt.DisplayRole or orientation == QtCore.Qt.Vertical:
            return None
        else:
            if section >= len(self.headers):
                return None
            else:
                _text = self.headers[section]
            return _text




class Selection_List_Model(QtCore.QAbstractItemModel):

    def __init__(self, items):
        self.catalog_content_dict = items
        self.headers = list(items[self.key_for_row(0)].keys())
        super().__init__()

    # def get_header_for_section(self, section):
    #     if section > len(self.items.keys()):
    #         return
    #     _keys = list(self.items.keys())
    #     _keys.insert(0, "Object Name")
    #     return _keys[section]
    #
    # def get_key_for_row(self, row):
    #     return list(self.items.keys())[row]

    # def data(self, index, role=None):
    #     _row = index.row()
    #     _column = index.column()
    #
    #     if _row > len(self.items.keys()):
    #         return
    #
    #     if role == QtCore.Qt.DisplayRole:
    #         return "Stuff"
    #
    #     if role == QtCore.Qt.DisplayRole:
    #         if _column == 0:
    #             return self.get_key_for_row(_row)
    #         else:
    #             return self.get_key_for_row(_row)[self.get_header_for_section(_column)]
    #
    # def rowCount(self, parent=None, *args, **kwargs):
    #     return 5
    #     return len(self.items.keys())
    #
    # def columnCount(self, parent=None, *args, **kwargs):
    #     return 6
    #     return len(self.get_key_for_row(0))
    #
    # def headerData(self, section, orientation, role=None):
    #     return "header"
    #     if orientation != QtCore.Qt.Vertical:
    #         if role == QtCore.Qt.DisplayRole:
    #             return self.get_header_for_section(section)
    #     return
    #
    # def index(self, row, column, parent=None, *args, **kwargs):
    #     if row > self.rowCount() or column > self.columnCount():
    #         return QtCore.QModelIndex()
    #     else:
    #         return self.createIndex(row, column)

    def key_for_row(self, row):
        """
        For the given row number will return the key
        that represents it in the data dictionary

        Parameters
        ----------
        row : int
            The row to get

        Returns
        -------
        str
            The key representing the given row

        """
        data_keys = list(self.catalog_content_dict.keys())
        return data_keys[row]

    def row_for_key(self, key):
        """
        Gets the row that the given key would take up

        Parameters
        ----------
        key : str
            The key to get the row value for (project name)

        Returns
        -------
        int
            The row number

        """
        _data_keys = list(self.catalog_content_dict.keys())
        for _row in range(0, self.rowCount()):
            if self.key_for_row(_row) == key:
                return _row

    def rowCount(self, parent=None, *args, **kwargs):
        """
        The amount of rows in the model

        Parameters
        ----------
        parent : QModelIndex
            Parent index
        args :
        kwargs :

        Returns
        -------
        int
            The amount of rows

        """
        return len(list(self.catalog_content_dict.keys()))

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Column amount is based on the amount of data given in the dict for each project

        Parameters
        ----------
        parent : QtCore.QModelIndex
            The parent model index -- not applicable in a table model
        args :
        kwargs :

        Returns
        -------
        int
            The amount of columns

        """
        _key_for_first_row = self.key_for_row(0)
        _dict_for_first_row = self.catalog_content_dict[_key_for_first_row]
        return len(_dict_for_first_row)

    def data(self, index, role=None):
        """
        Returns the data for the given index and role

        Parameters
        ----------
        index : QtCore.QModelIndex
            The index to get data for
        role : QtCore.Qt.Role
            The role to get data for

        Returns
        -------
        object
            The data for the given row and role

        """
        if role == QtCore.Qt.DisplayRole:
            _row = index.row()
            _column = index.column()

            _key_for_row = self.key_for_row(_row)       # project name -- is key for the main contents dict
            _dict_for_row = self.catalog_content_dict[_key_for_row]     # the dictionary for that given project
            _dict_key_list = list(_dict_for_row.values())       # list of that dicts values

            return _dict_key_list[_column]

    def headerData(self, section, orientation, role=None):
        """
        Returns the header data for the given index and role

        Parameters
        ----------
        section : int
            The index to get header data for.
        orientation : QtCore.Qt.Orientation
            The orientation of the header to get data for.
        role : QtCore.Qt.Role
            The role to get header data for.

        Returns
        -------
        object
            The header data for the given header index and row

        """
        if role != QtCore.Qt.DisplayRole or orientation == QtCore.Qt.Vertical:
            return None
        else:
            if section >= len(self.headers):
                return None
            else:
                _text = self.headers[section]
            return _text


class Table_Item_Selection_View(QtWidgets.QTableView):

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    from pyqt_interface_elements import base_windows
    import sys


    _app = QtWidgets.QApplication(sys.argv)
    _model = Selection_List_Model(
        {"item": {"name":"object", "item type": "type"}}
    )
    _view = Table_Item_Selection_View()
    #
    _view.setModel(_model)

    _win = base_windows.Main_Window()
    _win.setCentralWidget(_view)
    _win.show()

    sys.exit(_app.exec_())
