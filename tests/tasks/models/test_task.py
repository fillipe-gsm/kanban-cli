from datetime import datetime

import peewee as pw
import pytest

from config import settings
from src.tasks.models.category import Category
from src.tasks.models.task import Task


def test_can_create_task_with_not_long_name(tmp_db):
    assert Task.select().count() == 0, "Sanity check: no tasks yet"

    Task.create(title="buy milk")

    assert Task.select().count() == 1, "One task created"


def test_cannot_create_task_with_long_title(tmp_db):
    assert Task.select().count() == 0, "Sanity check: no tasks yet"

    long_title = "a" * (settings.task__title_max_length + 1)

    with pytest.raises(pw.IntegrityError):
        Task.create(title=long_title)

    assert Task.select().count() == 0, "Sanity check: still no tasks"


def test_can_create_task_with_category(tmp_db):
    category = Category.create(name="personal")
    task = Task.create(title="buy milk", category=category)

    assert task.category == category, "Task can have a category"


def test_can_create_task_with_creation_time(tmp_db):
    created_at = datetime(2020, 1, 1)
    task = Task.create(title="buy milk", created_at=created_at)

    assert task.created_at == created_at, "Creation date can be set"


def test_can_create_task_with_status(tmp_db):
    task1 = Task.create(title="buy milk", status=0)
    assert task1.status_str == settings.statuses[0], "Status is the first"

    task2 = Task.create(title="buy milk", status=2)
    assert task2.status_str == settings.statuses[2], "Status is the third"


def test_cannot_create_task_with_invalid_status(tmp_db):
    """Status must be a number within the possible statuses"""
    invalid_status = len(settings.statuses) + 1

    with pytest.raises(pw.IntegrityError):
        Task.create(title="buy milk", status=invalid_status)


def test_can_create_task_with_details(tmp_db):
    details = """
    # Something with markdown style
    A code:
    ```python
    import numpy as np
    ```
    """

    task = Task.create(title="buy milk", details=details)

    assert task.details == details


def test_group_by_status(tmp_db):
    """Tasks must be grouped by status and sorted by creation date"""
    cat1 = Category.create(name="cat1")
    cat2 = Category.create(name="cat2")
    # Notice some tasks have categories and some don't, and all of them must be
    # listed
    task1 = Task.create(
        title="t1", status=0, created_at=datetime(2020, 1, 6), category=cat1
    )
    task2 = Task.create(title="t2", status=0, created_at=datetime(2020, 1, 5))
    task3 = Task.create(title="t3", status=2, created_at=datetime(2020, 1, 4))
    task4 = Task.create(title="t4", status=3, created_at=datetime(2020, 1, 3))
    task5 = Task.create(title="t5", status=3, created_at=datetime(2020, 1, 2))
    task6 = Task.create(
        title="t6", status=1, created_at=datetime(2020, 1, 1), category=cat2
    )

    expected_tasks_by_status = {
        0: [task2, task1],
        1: [task6],
        2: [task3],
        3: [task5, task4],
    }

    tasks_by_status = Task.group_by_status()

    assert tasks_by_status == expected_tasks_by_status


def test_group_by_status__no_todos(tmp_db):
    tasks_by_status = Task.group_by_status()

    expected_tasks_by_status = {0: [], 1: [], 2: [], 3: []}

    assert tasks_by_status == expected_tasks_by_status
