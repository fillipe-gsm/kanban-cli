from io import StringIO

from rich.console import Console

from kanban_cli.categories.presenters.no_categories_presenter import (
    NoCategoriesPresenter,
)


def test_no_categories_presenter():
    console = Console(file=StringIO())

    presenter = NoCategoriesPresenter(console=console)
    presenter.present()

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]
    assert "No categories available." in console_output
