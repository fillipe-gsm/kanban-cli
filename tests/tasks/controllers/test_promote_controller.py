from unittest.mock import patch

import pytest

from config import settings
from src.tasks.controllers.promote_controller import promote_controller
from src.tasks.models.task import Task


@pytest.fixture
def mocked_view_all_controller():
    with patch(
        "src.tasks.controllers.promote_controller.view_all_controller"
    ) as m:
        yield m


def test_can_promote_a_task(tmp_db, mocked_view_all_controller):
    task1 = Task.create(title="buy milk", status=0)
    assert Task.get(Task.id == task1.id).status == 0, (
        "Sanity check: task being at level 0"
    )

    promote_controller(task_ids=[task1.id])

    assert Task.get(Task.id == task1.id).status == 1, "Task status moved up"
    mocked_view_all_controller.asssert_called_once()


def test_can_promote_multiple_tasks(tmp_db, mocked_view_all_controller):
    task1 = Task.create(title="task 1", status=0)
    task2 = Task.create(title="task 2", status=1)
    task3 = Task.create(title="task 3", status=2)

    promote_controller(task_ids=[task1.id, task2.id])

    mocked_view_all_controller.asssert_called_once()
    assert Task.get(Task.id == task1.id).status == 1, (
        f"Task {task1.id} status moved up"
    )
    assert Task.get(Task.id == task2.id).status == 2, (
        f"Task {task2.id} status moved up"
    )
    assert Task.get(Task.id == task3.id).status == 2, (
        f"Task {task3.id} status was unchanged"
    )


def test_cannot_promote_beyond_highest_status(
    tmp_db, mocked_view_all_controller
):
    last_status = len(settings.statuses) - 1
    task1 = Task.create(title="task 1", status=last_status)

    promote_controller(task_ids=[task1.id])

    mocked_view_all_controller.asssert_called_once()
    assert Task.get(Task.id == task1.id).status == last_status, (
        "Cannot move beyond last status"
    )


def test_non_existing_tasks_are_silently_ignored(
    tmp_db, mocked_view_all_controller
):
    task1 = Task.create(title="task 1", status=0)

    # 2 and 3 are ids of non-existing todos
    promote_controller(task_ids=[task1.id, 2, 3])

    # It should succeed with no issues
    assert Task.get(Task.id == task1.id).status == 1, (
        f"Task {task1.id} status moved up"
    )
    mocked_view_all_controller.asssert_called_once()
