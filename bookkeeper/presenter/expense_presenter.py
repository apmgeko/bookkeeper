class ExpensePresenter():
    def __init__(self, model, view, cat_repo, exp_repo) -> None:
        self.view = view
        self.model = model
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.exp_data = exp_repo.get_all()
        self.cat_data = cat_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_add_expense_button_clicked)
        #self.view.on_expense_delete_button_clicked(self.handle_expense_delete_button_clicked)
        #self.view.on_category_edit_button_clicked(self.handle_category_edit_button_clicked)

    def update_expense_data(self) -> None:
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = self.cat_repo.get_all()
        for e in self.exp_data:
            cat = self.cat_repo.get(e.category)
            e.category = cat.name
        self.view.set_category_dropdown(self.cat_data)
        self.view.set_expense_table(self.exp_data)

    def show(self) -> None:
        self.view.show()
        self.update_expense_data()

    def handle_add_expense_button_clicked(self) -> None:
        amount = self.view.get_amount()
        cat_pk = self.view.get_selected_cat()
        exp = self.exp_repo.cls(amount, cat_pk)
        self.exp_repo.add(exp)
        self.update_expense_data()
    
