from unittest.mock import patch

import pytest

from kanban_cli.categories.models.category import Category
from kanban_cli.tasks.controllers.edit_controller import edit_controller
from kanban_cli.tasks.models.task import Task
from kanban_cli.tasks.presenters.no_task_presenter import NoTaskPresenter
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


@pytest.fixture
def mocked_view_all_controller():
    with patch("kanban_cli.tasks.controllers.edit_controller.view_controller") as m:
        yield m


@pytest.fixture
def mocked_no_task_presenter():
    with patch.object(NoTaskPresenter, "present") as m:
        yield m


def test_no_tasks_exist(
    tmp_db, mocked_no_task_presenter, mocked_view_all_controller
):
    """As no tasks exist, we should see the appropriate message"""
    edit_controller(task_id=1)

    mocked_no_task_presenter.assert_called_once()
    mocked_view_all_controller.assert_not_called()


def test_edit_defaults(
    tmp_db,
    mocked_no_task_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    """Test we get an updated task with no changes"""
    category = Category.create(name="category")
    task = Task.create(
        title="Buy milk",
        status=1,
        priority=1,
        category=category,
        details="Buy milk because...",
    )
    assert Category.select().count() == 1, "sanity check: one category exists"

    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept title
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept status
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept priority
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept category
    mocked_prompt_input.send_text(
        KEY_MAPPINGS["<Enter>"]
    )  # don't edit details

    with mock_app_session:
        edit_controller(task_id=task.id)

    edited_task = Task.get_by_id(pk=task.id)

    # Sanity check: no property got changed
    assert edited_task.title == task.title
    assert edited_task.status == task.status
    assert edited_task.priority == task.priority
    assert edited_task.category == task.category
    assert edited_task.details == task.details
    assert Category.select().count() == 1, (
        "sanity check: no new category was created"
    )


def test_edit_defaults__can_update_attribute(
    tmp_db,
    mocked_no_task_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    category = Category.create(name="category")
    task = Task.create(
        title="Buy milk",
        status=1,
        priority=1,
        category=category,
        details="Buy milk becausi",  # with a typo at the last character
    )
    assert Category.select().count() == 1, "sanity check: one category exists"

    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept title
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept status
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept priority
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept category

    # For details: press "Down" to select "yes"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Press backspace to fix the typo and add a couple more characters
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Backspace>"])
    mocked_prompt_input.send_text("e...")
    # Press Esc+Enter to confirm
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Esc>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        edit_controller(task_id=task.id)

    edited_task = Task.get_by_id(pk=task.id)

    # Sanity check: no property but the details got changed
    assert edited_task.title == task.title
    assert edited_task.status == task.status
    assert edited_task.priority == task.priority
    assert edited_task.category == task.category
    assert edited_task.details == "Buy milk because...", "details got updated"
    assert Category.select().count() == 1, (
        "sanity check: no new category was created"
    )


def test_edit_defaults__can_update_category(
    tmp_db,
    mocked_no_task_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    category = Category.create(name="category 1")
    task = Task.create(
        title="Buy milk",
        status=1,
        priority=1,
        category=category,
    )
    assert Category.select().count() == 1, "sanity check: one category exists"

    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept title
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept status
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])  # accept priority

    # Edit category name
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Backspace>"])
    mocked_prompt_input.send_text("2")  # edit to "category 2"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    mocked_prompt_input.send_text(
        KEY_MAPPINGS["<Enter>"]
    )  # don't change details

    with mock_app_session:
        edit_controller(task_id=task.id)

    edited_task = Task.get_by_id(pk=task.id)

    assert Category.select().count() == 2, "one new category was created"
    assert edited_task.category_name == "category 2"

    # Sanity check: no property but the category got changed
    assert edited_task.title == task.title
    assert edited_task.status == task.status
    assert edited_task.priority == task.priority
    assert edited_task.details == task.details
