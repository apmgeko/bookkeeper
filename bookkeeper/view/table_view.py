import datetime
from inspect import get_annotations
from PySide6 import QtCore

class TableModel(QtCore.QAbstractTableModel):
    """
    Class for table visualisation of abstract classes via GUI
    """
    def __init__(self, cls, data) -> None:
        super(TableModel, self).__init__()
        self._data = data
        self.en_ru = {'amount': 'Стоимость, руб.',
             'category': 'Категория',
             'expense_date': 'Дата',
             'added_date': 'Добавлено',
             'comment': 'Комментарий',
             'pk': 'ID',
             'period': 'Период',
             'lim': 'Макс. сумма',
             'spent': 'Потрачено'}
        self.cls = cls
        header_data = get_annotations(cls, eval_str=True)
        self.header_names = list(self.en_ru[word] for word in header_data)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role) -> str | None:
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            val = self._data[index.row()].__getattribute__(fields[index.column()])
            if isinstance(val, datetime.datetime):
                val = str(val)[:19] # cut to YYYY-MM-DD hh:mm:ss format
            return val
        
    def get_row(self, row) -> list:
        val = self._data[row]
        return val

    def rowCount(self, index) -> int:
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index) -> int:
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data == []:
            return 0
        return len(self._data[0].__dataclass_fields__)
