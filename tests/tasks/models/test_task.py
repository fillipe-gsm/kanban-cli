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


def test_category_name__existing_category(tmp_db):
    category_name = "cat"
    category = Category.create(name=category_name)
    task = Task.create(title="buy milk", category=category)

    assert task.category_name == category_name


def test_category_name__nonexisting_category(tmp_db):
    task = Task.create(title="buy milk")

    assert task.category_name == Task.NO_CATEGORY_STR


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


def test_add_from_prompt(tmp_db):
    title = "buy milk"
    status = 0
    category_name = "category"
    details = "Buy a lot of milk"

    task = Task.add_from_prompt(title, status, category_name, details)

    assert Task.select().count() == 1, "A task has been created"
    assert Category.select().count() == 1, "A new category has been created"
    assert task.title == title
    assert task.status == status
    assert task.category.name == category_name
    assert task.details == details


def test_add_from_prompt__empty_category(tmp_db):
    title = "buy milk"
    status = 0
    category_name = ""
    details = "Buy a lot of milk"

    task = Task.add_from_prompt(title, status, category_name, details)

    assert Task.select().count() == 1, "A task has been created"
    assert Category.select().count() == 0, "No category has been created"
    assert task.title == title
    assert task.status == status
    assert task.category is None
    assert task.details == details


def test_add_from_prompt__does_not_recreate_existing_categories(tmp_db):
    Category.create(name="category")  # say a category already exists
    assert Category.select().count() == 1, "Sanity check: one category exists"

    title = "buy milk"
    status = 0
    category_name = "category"
    details = "Buy a lot of milk"

    task = Task.add_from_prompt(title, status, category_name, details)

    assert Task.select().count() == 1, "A task has been created"
    assert Category.select().count() == 1, "No new category is created"
    assert task.title == title
    assert task.status == status
    assert task.category.name == category_name
    assert task.details == details


def test_edit_from_prompt__no_changes(tmp_db):
    category = Category.create(name="category")
    task = Task.create(
        title="Buy milk", status=1, category=category, details="More stuff"
    )
    assert Category.select().count() == 1, "Sanity check: one category exists"

    task.edit_from_prompt(
        title=task.title,
        status=task.status,
        category_name=task.category_name,
        details=task.details,
    )

    edited_task = Task.get_by_id(pk=task.id)

    assert edited_task.title == task.title
    assert edited_task.category == task.category
    assert edited_task.status == task.status
    assert edited_task.details == task.details
    assert Category.select().count() == 1, "No new category was created"


def test_edit_from_prompt__can_change_properties(tmp_db):
    category = Category.create(name="category")
    task = Task.create(
        title="Buy milk", status=1, category=category, details="More stuff"
    )
    assert Category.select().count() == 1, "Sanity check: one category exists"

    new_title = "Buy milk edited"
    new_status = 2
    new_details = "More stuff edited"
    task.edit_from_prompt(
        title=new_title,
        status=new_status,
        category_name=task.category_name,  # unchanged
        details=new_details,
    )

    edited_task = Task.get_by_id(pk=task.id)

    assert edited_task.title == new_title
    assert edited_task.category == task.category, "Category was unchanged"
    assert edited_task.status == new_status
    assert edited_task.details == new_details
    assert Category.select().count() == 1, "No new category was created"


def test_edit_from_prompt__can_change_category(tmp_db):
    category = Category.create(name="category")
    task = Task.create(
        title="Buy milk", status=1, category=category, details="More stuff"
    )
    assert Category.select().count() == 1, "Sanity check: one category exists"

    new_category_name = "category 2"
    task.edit_from_prompt(
        title=task.title,
        status=task.status,
        category_name=new_category_name,
        details=task.details,
    )

    edited_task = Task.get_by_id(pk=task.id)

    assert edited_task.title == task.title, "title is unchaged"
    assert edited_task.status == task.status, "status is unchanged"
    assert edited_task.details == task.details, "details is unchanged"
    assert edited_task.category_name == new_category_name, (
        "category was changed"
    )
    assert Category.select().count() == 2, "one new category has been created"


def test_promote__can_promote_a_task(tmp_db):
    task = Task.create(title="buy milk", status=0)

    Task.promote(task_ids=[task.id])
    promoted_task = Task.get_by_id(pk=task.id)

    assert promoted_task.status == 1, "status moved up"


def test_promote__can_promote_multiple_tasks(tmp_db):
    task1 = Task.create(title="task 1", status=0)
    task2 = Task.create(title="task 2", status=1)
    task3 = Task.create(title="task 3", status=2)

    Task.promote(task_ids=[task1.id, task2.id])

    assert Task.get_by_id(task1.id).status == 1, (
        f"Task {task1.id} status moved up"
    )
    assert Task.get_by_id(task2.id).status == 2, (
        f"Task {task2.id} status moved up"
    )
    assert Task.get_by_id(task3.id).status == 2, (
        f"Task {task3.id} status was unchanged"
    )


def test_promote__cannot_promote_beyond_highest_status(tmp_db):
    last_status = len(settings.statuses) - 1
    task = Task.create(title="task 1", status=last_status)

    Task.promote(task_ids=[task.id])

    assert Task.get_by_id(pk=task.id).status == last_status, (
        "Cannot move beyond last status"
    )


def test_promote__non_existing_tasks_are_silently_ignored(tmp_db):
    task = Task.create(title="task 1", status=0)

    # 2 and 3 are ids of non-existing todos
    Task.promote(task_ids=[task.id, 2, 3])

    # It should succeed with no issues
    assert Task.get_by_id(pk=task.id).status == 1, (
        f"Task {task.id} status moved up"
    )
