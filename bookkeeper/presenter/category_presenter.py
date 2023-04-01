class CategoryPresenter():
    """
    Class for presenting categories in GUI
    """
    def __init__(self, model, view, cat_repo) -> None:
        self.view = view
        self.model = model
        self.cat_repo = cat_repo
        self.cat_data = cat_repo.get_all()
        self.view.on_add_category_button_clicked(
            self.handle_add_category_button_clicked
            )
        self.view.on_delete_category_button_clicked(
            self.handle_delete_category_button_clicked
            )

    def update_categories(self):
        self.view.set_category_dropdown(self.cat_repo.get_all())
        self.view.importData()
        self.view.tree.expandAll()

    def handle_add_category_button_clicked(self):
        name = self.view.get_name()
        if self.cat_repo.get_all(where={'name': name}) != []:
            raise ValueError('Категория с таким названием уже существует!')
        parent_cat_pk = self.view.get_selected_cat()
        if parent_cat_pk == 0:
            parent_cat_pk = None
        cat = self.cat_repo.cls(name, parent_cat_pk)
        self.cat_repo.add(cat)
        self.update_categories()

    def i_will_kill_you_and_all_your_children_too(self, cat_pk):
        child_list = self.cat_repo.get_all(where={'parent': cat_pk})
        if child_list == []:
            self.cat_repo.delete(cat_pk)
        else:
            for child in child_list:
                self.i_will_kill_you_and_all_your_children_too(child.pk)
            self.cat_repo.delete(cat_pk)

    def handle_delete_category_button_clicked(self):
        cat_pk = self.view.get_clicked_category()
        self.i_will_kill_you_and_all_your_children_too(cat_pk)
        self.update_categories()

    def show(self):
        self.view.set_category_dropdown(self.cat_repo.get_all())
        self.update_categories()
        self.view.exec_()
