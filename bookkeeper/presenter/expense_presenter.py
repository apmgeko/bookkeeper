class ExpensePresenter():
    """
    Class for expenses visualisation via GUI
    """
    def __init__(self, model, view, cat_repo, exp_repo, budget_repo) -> None:
        self.view = view
        self.model = model
        self.budget_repo = budget_repo
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.view.on_expense_add_button_clicked(
            self.handle_add_expense_button_clicked
            )
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked
            )
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
            )
        self.view.on_budget_add_button_clicked(
            self.handle_budget_add_button_clicked
            )
        self.view.on_budget_delete_button_clicked(
            self.handle_budget_delete_button_clicked
            )

    def update_expense_data(self) -> None:
        """
        Class for expenses visualisation via GUI
        """
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = self.cat_repo.get_all()
        self.budget_data = self.budget_repo.get_all()
        self.show_category_names()
        self.update_budget_data()
        self.view.set_category_dropdown(self.cat_data)
        self.view.set_period_dropdown(self.budget_data)
        self.view.set_expense_table(self.exp_data)
        self.view.set_budget_table(self.budget_data)

    def show_category_names(self) -> None:
        for e in self.exp_data:
            cat = self.cat_repo.get(e.category)
            e.category = cat.name

    def update_budget_data(self) -> None:
        for budget in self.budget_data:
            budget.update(self.exp_repo)
            self.budget_repo.update(budget)
        self.budget_data = self.budget_repo.get_all()

    def show(self) -> None:
        self.update_expense_data()
        self.view.show()

    def handle_add_expense_button_clicked(self) -> None:
        amount = self.view.get_amount()
        cat_pk = self.view.get_selected_cat()
        exp = self.exp_repo.cls(amount, cat_pk)
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_category_edit_button_clicked(self):
        self.view.show_cats_dialog(self.cat_repo)
        self.view.set_category_dropdown(self.cat_repo.get_all())

    def handle_expense_delete_button_clicked(self) -> None:
        exp_pk = self.view.get_selected_expense()
        self.exp_repo.delete(exp_pk)
        self.update_expense_data()

    def handle_budget_add_button_clicked(self) -> None:
        lim = self.view.get_lim()
        period = self.view.get_selected_period()
        if self.budget_repo.get_all(where={'period': period}) != []:
            raise ValueError("Бюджет на этот срок уже установлен!")
        budget = self.budget_repo.cls(period, lim)
        self.budget_repo.add(budget)
        self.update_budget_data()
        self.update_expense_data()

    def handle_budget_delete_button_clicked(self) -> None:
        budget_pk = self.view.get_selected_budget()
        self.budget_repo.delete(budget_pk)
        self.update_expense_data()
