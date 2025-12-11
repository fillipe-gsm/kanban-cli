from unittest.mock import patch

import pytest

from kanban_cli.tasks.controllers.view_controller import view_controller
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.no_task_presenter import NoTaskPresenter
from kanban_cli.tasks.presenters.view_presenter import ViewPresenter


@pytest.fixture
def mocked_no_task_presenter():
    with patch.object(NoTaskPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_view_presenter():
    with patch.object(ViewPresenter, "present") as m:
        yield m


def test_no_tasks_exist(
    tmp_db, mocked_no_task_presenter, mocked_view_presenter
):
    """As no tasks exist, we should see the appropriate message"""
    view_controller(task_id=1)

    mocked_no_task_presenter.assert_called_once()
    mocked_view_presenter.assert_not_called()


def test_tasks_exist(tmp_db, mocked_no_task_presenter, mocked_view_presenter):
    task = Task.create(title="task1")

    view_controller(task_id=task.id)

    # As there is a task, it calls the "view task presenter"
    mocked_no_task_presenter.assert_not_called()
    mocked_view_presenter.assert_called_once()
