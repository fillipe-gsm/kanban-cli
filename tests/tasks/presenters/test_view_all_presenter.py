from datetime import datetime
from io import StringIO

from rich.console import Console

from kanban_cli.categories.models.category import Category
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.view_all_presenter import ViewAllPresenter


def test_present(tmp_db):
    cat1 = Category.create(name="cat1")
    cat2 = Category.create(name="cat2")
    # Notice some tasks have categories and some don't, and all of them must be
    # listed
    task1 = Task.create(
        title="Buy milk",
        status=0,
        created_at=datetime(2020, 1, 6),
        category=cat1,
    )
    task2 = Task.create(
        title="Paint the walls", status=0, created_at=datetime(2020, 1, 5)
    )
    task3 = Task.create(
        title="Swept the floor",
        status=2,
        created_at=datetime(2020, 1, 4),
    )
    task4 = Task.create(
        title="Make excuses", status=3, created_at=datetime(2020, 1, 3)
    )
    task5 = Task.create(
        title="Gamed for two minutes",
        status=3,
        created_at=datetime(2020, 1, 2),
    )
    task6 = Task.create(
        title="Procrastinating",
        status=1,
        created_at=datetime(2020, 1, 1),
        category=cat2,
    )
    tasks_by_status = Task.group_by_status()

    # Enforce terminal width long enough so no text is wrapped and the
    # assertions do not show false negatives
    console = Console(file=StringIO(), width=200)

    presenter = ViewAllPresenter(console=console)
    presenter.present(tasks_by_status)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]

    # For tasks with category, the id, category name, priority and title are
    # shown
    for task in (task1, task6):
        assert str(task.id) in console_output
        assert task.category.name in console_output
        assert task.priority_str in console_output
        assert task.title in console_output

    # For tasks without category, the id, priority and title are shown, plus a
    # generic "No category" message
    for task in (task2, task3, task4, task5):
        assert str(task.id) in console_output
        assert ViewAllPresenter.NO_CATEGORY_STR in console_output
        assert task.priority_str in console_output
        assert task.title in console_output


def test_present__empty_tasks_in_status(tmp_db):
    """Fixes a bug where the code fails if some statues have no tasks"""
    category = Category.create(name="cat1")
    # Only one task in the status 0
    task = Task.create(
        title="Buy milk",
        status=0,
        category=category,
    )
    tasks_by_status = Task.group_by_status()

    console = Console(file=StringIO(), width=200)
    presenter = ViewAllPresenter(console=console)
    presenter.present(tasks_by_status)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]

    assert task.title in console_output, "Existing task is in output"
