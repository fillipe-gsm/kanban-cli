from io import StringIO

from rich.console import Console

from kanban_cli.categories.presenters.no_category_presenter import NoCategoryPresenter


def test_no_tasks_presenter():
    console = Console(file=StringIO())

    presenter = NoCategoryPresenter(console=console)
    presenter.present(category_id=1)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]
    assert "No category exists with id #1." in console_output
