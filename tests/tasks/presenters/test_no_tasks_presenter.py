from io import StringIO

from rich.console import Console

from kanban_cli.tasks.presenters.no_tasks_presenter import NoTasksPresenter


def test_no_tasks_presenter():
    console = Console(file=StringIO())

    presenter = NoTasksPresenter(console=console)
    presenter.present()

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]
    assert "No tasks available." in console_output
