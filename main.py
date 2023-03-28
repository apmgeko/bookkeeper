import sys
from PySide6 import QtWidgets
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository

db_file = 'database.db'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    view = MainWindow()
    model = None

    cat_repo = SQLiteRepository(db_file, Category)
    exp_repo = SQLiteRepository(db_file, Expense)
    budget_repo = SQLiteRepository(db_file, Budget)

    window = ExpensePresenter(model, view, cat_repo, exp_repo, budget_repo)
    window.show()

    sys.exit(app.exec())