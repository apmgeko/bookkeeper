from PySide6 import QtCore, QtWidgets
import datetime

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        print('data =', data)
        self.en_ru = {'amount': 'Стоимость',
             'category': 'Категория',
             'expense_date': 'Дата',
             'added_date': 'Добавлено',
             'comment': 'Комментарий',
             'pk': 'ID покупки'}
        dt = data[0].__dataclass_fields__.keys()
        self.header_names = list(self.en_ru[word] for word in dt)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            val = self._data[index.row()].__getattribute__(fields[index.column()])
            if type(val) == datetime.datetime:
                val = str(val)[:19] # cut to YYYY-MM-DD hh:mm:ss format
            return val

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0].__dataclass_fields__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.model = None
        self.setWindowTitle('Банковский учет')
        self.resize(700, 500)

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(QtWidgets.QLabel('Последние расходы'))
        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QtWidgets.QLabel('Бюджет'))
        self.budget_grid = QtWidgets.QTableView() #TODO: таблица бюджета
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QtWidgets.QGridLayout()

        self.bottom_controls.addWidget(QtWidgets.QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QtWidgets.QLineEdit()
        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)  # TODO: добавить валидатор
        self.bottom_controls.addWidget(QtWidgets.QLabel('Категория'), 1, 0)

        self.category_dropdown = QtWidgets.QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QtWidgets.QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)
        #self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.expense_add_button = QtWidgets.QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.expense_delete_button = QtWidgets.QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 2, 2)  #TODO: improve buttons layout

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
    
    def set_expense_table(self, data):
        self.item_model = TableModel(data)
        self.expenses_grid.setModel(self.item_model)
    
    def set_category_dropdown(self, data):
        for cat in data:
            self.category_dropdown.addItem(cat.name, cat.pk)

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def get_amount(self):
        amount = self.amount_line_edit.text()
        if not amount.isdigit() or int(amount) < 0:
            raise ValueError("Введенная сумма должна быть неотрицательным целым числом.")
        return int(amount)
    
    def get_selected_cat(self) -> int:
        idx = self.category_dropdown.currentIndex()
        cat_pk = self.category_dropdown.itemData(idx)
        return cat_pk