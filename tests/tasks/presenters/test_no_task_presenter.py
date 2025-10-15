from io import StringIO

from rich.console import Console

from src.tasks.presenters.no_task_presenter import NoTaskPresenter


def test_no_tasks_presenter():
    console = Console(file=StringIO())

    presenter = NoTaskPresenter(console=console)
    presenter.present(task_id=1)

    assert "No task exists with id #1." in console.file.getvalue()
