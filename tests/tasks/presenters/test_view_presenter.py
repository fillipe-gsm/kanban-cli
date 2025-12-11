from io import StringIO

from rich.console import Console

from kanban_cli.categories.models.category import Category
from kanban_cli.config import settings
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.view_presenter import ViewPresenter


def test_present(tmp_db):
    category = Category.create(name="category")
    task = Task.create(title="buy milk", category=category)

    console = Console(file=StringIO(), width=200)
    presenter = ViewPresenter(console=console)
    presenter.present(task)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]

    assert str(task.id) in console_output
    assert task.title in console_output
    assert settings.statuses[task.status] in console_output
    assert settings.priorities[task.priority] in console_output
    assert task.category.name in console_output


def test_present__no_category(tmp_db):
    task = Task.create(title="buy milk")

    console = Console(file=StringIO(), width=200)
    presenter = ViewPresenter(console=console)
    presenter.present(task)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]

    assert str(task.id) in console_output
    assert task.title in console_output
    assert settings.statuses[task.status] in console_output
    assert settings.priorities[task.priority] in console_output
    assert task.NO_CATEGORY_STR in console_output


def test_present__with_details(tmp_db):
    details = "# Something important in markdown"
    task = Task.create(title="buy milk", details=details)

    console = Console(file=StringIO(), width=200)
    presenter = ViewPresenter(console=console)
    presenter.present(task)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]

    assert str(task.id) in console_output
    assert task.title in console_output
    assert settings.statuses[task.status] in console_output
    assert settings.priorities[task.priority] in console_output
    assert task.NO_CATEGORY_STR in console_output
    assert task.details in console_output
