from io import StringIO

from rich.console import Console

from src.tasks.presenters.no_tasks_presenter import NoTasksPresenter


def test_no_tasks_presenter(tmp_db):
    console = Console(file=StringIO())

    presenter = NoTasksPresenter(console=console)
    presenter.present()

    assert "No tasks available." in console.file.getvalue()
