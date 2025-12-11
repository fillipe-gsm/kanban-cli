from unittest.mock import patch

import pytest

from kanban_cli.tasks.controllers.delete_controller import delete_controller
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.no_task_presenter import NoTaskPresenter
from kanban_cli.tasks.presenters.view_all_presenter import ViewAllPresenter
from kanban_cli.tasks.presenters.view_presenter import ViewPresenter
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


@pytest.fixture
def mocked_no_task_presenter():
    with patch.object(NoTaskPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_view_presenter():
    with patch.object(ViewPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_view_all_presenter():
    with patch.object(ViewAllPresenter, "present") as m:
        yield m


def test_no_tasks_exist(
    tmp_db,
    mocked_no_task_presenter,
    mocked_view_presenter,
    mocked_view_all_presenter,
):
    """
    As no tasks exist, we should see the appropriate message and not delete
    anything
    """
    task = Task.create(title="buy milk")

    assert Task.select().count() == 1, "Sanity check: one task exists"

    delete_controller(task_id=task.id + 1)  # calls non-existing id
    assert Task.select().count() == 1, "Sanity check: the task still exists"

    mocked_no_task_presenter.assert_called_once()
    mocked_view_presenter.assert_not_called()
    mocked_view_all_presenter.assert_not_called()


def test_task_exists_and_is_not_deleted(
    tmp_db,
    mocked_no_task_presenter,
    mocked_view_presenter,
    mocked_view_all_presenter,
    mocked_prompt_input,
    mock_app_session,
):
    task1 = Task.create(title="task1")
    Task.create(title="task2")
    assert Task.select().count() == 2, "Sanity check: two tasks exist"

    # Press Enter directly to select "no"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        delete_controller(task_id=task1.id)

    assert Task.select().count() == 2, "Two tasks still exist"

    # Also, only the view presenters is called to confirm the deletion
    mocked_no_task_presenter.assert_not_called()
    mocked_view_presenter.assert_called_once()
    mocked_view_all_presenter.assert_called_once()


def test_task_exists_and_gets_deleted(
    tmp_db,
    mocked_no_task_presenter,
    mocked_view_presenter,
    mocked_view_all_presenter,
    mocked_prompt_input,
    mock_app_session,
):
    task1 = Task.create(title="task1")
    task2 = Task.create(title="task2")
    assert Task.select().count() == 2, "Sanity check: two tasks exist"

    # Press down once to select "yes"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        delete_controller(task_id=task1.id)

    remaining_tasks = list(Task.select())
    assert len(remaining_tasks) == 1, "Only one task exists now"
    assert remaining_tasks[0].id == task2.id

    # Also, only the view presenters is called to confirm the deletion
    mocked_no_task_presenter.assert_not_called()
    mocked_view_presenter.assert_called_once()
    mocked_view_all_presenter.assert_called_once()
