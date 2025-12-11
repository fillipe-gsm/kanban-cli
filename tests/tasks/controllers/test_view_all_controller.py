from unittest.mock import patch

import pytest

from kanban_cli.tasks.controllers.view_all_controller import (
    view_all_controller,
)
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.no_tasks_presenter import NoTasksPresenter
from kanban_cli.tasks.presenters.view_all_presenter import ViewAllPresenter


@pytest.fixture
def mocked_no_tasks_presenter():
    with patch.object(NoTasksPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_view_all_presenter():
    with patch.object(ViewAllPresenter, "present") as m:
        yield m


def test_no_tasks_exist(
    tmp_db, mocked_no_tasks_presenter, mocked_view_all_presenter
):
    view_all_controller()

    # As there are no tasks, it calls the "no tasks presenter"
    mocked_no_tasks_presenter.assert_called_once()
    mocked_view_all_presenter.assert_not_called()


def test_tasks_exist(
    tmp_db, mocked_no_tasks_presenter, mocked_view_all_presenter
):
    Task.create(title="task1")
    Task.create(title="task2", status=1)

    view_all_controller()

    # As there are tasks, it calls the "view all tasks presenter"
    mocked_no_tasks_presenter.assert_not_called()
    mocked_view_all_presenter.assert_called_once()
