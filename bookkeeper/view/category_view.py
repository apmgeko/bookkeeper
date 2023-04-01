from collections import deque
from PySide6 import QtWidgets
from PySide6.QtGui import *


class CategoryDialog(QtWidgets.QDialog):
    """
    Class for category visualisation via GUI
    """
    def __init__(self, cat_repo) -> None:
        super().__init__()
        self.cat_repo = cat_repo
        self.setup()
        self.importData()
        self.tree.expandAll()

    def show_cat_tree(self):
        """
        Visualisation of category tree
        """
        self.tree = QtWidgets.QTreeView(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        return layout
                    
    def setup(self):
        """
        Help function for class initialisation
        """
        self.setWindowTitle('Редактирование категорий')
        self.setGeometry(300, 100, 600, 300)

        self.layout = QtWidgets.QVBoxLayout()
        layout = self.show_cat_tree()

        self.bottom_options = QtWidgets.QGridLayout()
        self.add_category_button = QtWidgets.QPushButton('Добавить')
        self.bottom_options.addWidget(self.add_category_button, 1, 0, 1, 2)
        self.delete_category_button = QtWidgets.QPushButton('Удалить')
        self.bottom_options.addWidget(self.delete_category_button, 1, 2, 1, 2)

        self.category_dropdown = QtWidgets.QComboBox()
        self.new_category_line_edit = QtWidgets.QLineEdit()
        self.bottom_options.addWidget(self.new_category_line_edit, 0, 1)
        self.bottom_options.addWidget(QtWidgets.QLabel('Категория'), 0, 0)
        self.bottom_options.addWidget(self.category_dropdown, 0, 3)
        self.bottom_options.addWidget(QtWidgets.QLabel('Надкатегория'), 0, 2)

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setLayout(self.bottom_options)
        layout.addWidget(self.bottom_widget)

    def importData(self, root=None):
        """
        Method to build the tree from import data
        """
        data = self.cat_repo.get_all()
        data = [{'unique_id': c.pk, 'category_name': c.name, 'parent_id': c.parent} for c in data]
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value['parent_id'] is None:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([QStandardItem(value['category_name'])])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

    def set_category_dropdown(self, data):
        """
        Fills in category dropdown menu from cat_repo
        """
        self.category_dropdown.clear()
        self.category_dropdown.addItem('', 0)
        for cat in data:
            self.category_dropdown.addItem(cat.name, cat.pk)
                    
    def on_add_category_button_clicked(self, slot):
        """
        This method executes when add_category_button is clicked
        """
        self.add_category_button.clicked.connect(slot)
            
    def on_delete_category_button_clicked(self, slot):
        """
        This method executes when delete_category_button is clicked
        """
        self.delete_category_button.clicked.connect(slot)

    def get_name(self):
        """
        Extract added category name from new_category_line_edit
        """
        name = self.new_category_line_edit.text()
        if name == '':
            raise ValueError("Название категории не может быть пустым.")
        return name

    def get_selected_cat(self) -> int:
        """
        Extract selected category pk from category dropdown menu
        """
        idx = self.category_dropdown.currentIndex()
        cat_pk = self.category_dropdown.itemData(idx)
        return cat_pk

    def get_clicked_category(self) -> int:
        """
        Extract clicked category pk from category tree
        """
        idx = self.tree.currentIndex()
        cat_name = idx.model().itemFromIndex(idx).text()
        cat_pk = self.cat_repo.get_all(where={'name': cat_name})[0].pk
        return cat_pk
    