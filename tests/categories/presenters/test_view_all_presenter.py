from io import StringIO

from rich.console import Console

from kanban_cli.categories.models.category import Category
from kanban_cli.categories.presenters.view_all_presenter import ViewAllPresenter


def test_present(tmp_db):
    category1 = Category.create(name="cat1")
    category2 = Category.create(name="cat2")

    console = Console(file=StringIO())

    presenter = ViewAllPresenter(console=console)
    presenter.present(Category.list_categories())

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]

    for category in (category1, category2):
        assert str(category.id) in console_output, "id is in the output"
        assert str(category.name) in console_output, "name is in the output"
