from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from kanban_cli.app.app import create_app
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.no_task_presenter import NoTaskPresenter
from kanban_cli.tasks.presenters.no_tasks_presenter import NoTasksPresenter

runner = CliRunner()


@pytest.fixture
def tst_app():
    return create_app()


def test_view_all(tst_app, tmp_db):
    task1 = Task.create(title="buy milk")
    task2 = Task.create(title="buy bread")

    result = runner.invoke(tst_app, ["tasks", "view-all"])

    assert result.exit_code == 0, "sanity check: no errors"
    # Existing tasks are in displayed output
    for task in (task1, task2):
        assert str(task.id) in result.output
        assert task.title in result.output


def test_view_all__no_tasks(tst_app, tmp_db):
    result = runner.invoke(tst_app, ["tasks", "view-all"])

    assert result.exit_code == 0, "sanity check: no errors"
    assert NoTasksPresenter.MSG in result.output, "shows no tasks presenter"


def test_view_task(tst_app, tmp_db):
    task = Task.create(title="buy milk", details="why buy milk")

    result = runner.invoke(tst_app, ["tasks", "view", f"{task.id}"])

    assert result.exit_code == 0, "sanity check: no errors"
    # Existing task is in displayed output
    assert str(task.id) in result.output
    assert task.title in result.output
    assert task.details in result.output


def test_view_task__non_existing_task(tst_app, tmp_db):
    result = runner.invoke(tst_app, ["tasks", "view", "1"])

    assert result.exit_code == 0, "sanity check: no errors"
    expected_msg = NoTaskPresenter.MSG.format(1)
    assert expected_msg in result.output


def test_add(tst_app, tmp_db):
    with patch("kanban_cli.tasks.tasks_app.add_controller") as m:
        runner.invoke(tst_app, ["tasks", "add"])

    # Add controller was called
    m.assert_called_once()


def test_edit(tst_app, tmp_db):
    task_id = 1
    with patch("kanban_cli.tasks.tasks_app.edit_controller") as m:
        runner.invoke(tst_app, ["tasks", "edit", f"{task_id}"])

    # Add controller was called
    m.assert_called_once_with(task_id)


def test_delete(tst_app, tmp_db):
    task_id = 1
    with patch("kanban_cli.tasks.tasks_app.delete_controller") as m:
        runner.invoke(tst_app, ["tasks", "delete", f"{task_id}"])

    # Add controller was called with task_id
    m.assert_called_once_with(task_id)


def test_promote(tst_app, tmp_db):
    task_ids = [1, 2]
    with patch("kanban_cli.tasks.tasks_app.promote_controller") as m:
        runner.invoke(
            tst_app, ["tasks", "promote", str(task_ids[0]), str(task_ids[1])]
        )

    # Add controller was called
    m.assert_called_once_with(task_ids)


def test_regress(tst_app, tmp_db):
    task_ids = [1, 2]
    with patch("kanban_cli.tasks.tasks_app.regress_controller") as m:
        runner.invoke(
            tst_app, ["tasks", "regress", str(task_ids[0]), str(task_ids[1])]
        )

    # Add controller was called
    m.assert_called_once_with(task_ids)
