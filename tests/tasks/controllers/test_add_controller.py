from unittest.mock import patch

import pytest

from src.tasks.controllers.add_controller import add_controller
from src.tasks.models.category import Category
from src.tasks.models.task import Task
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


@pytest.fixture
def mocked_view_all_controller():
    with patch(
        "src.tasks.controllers.add_controller.view_all_controller"
    ) as m:
        yield m


def test_add_controller(
    tmp_db, mock_app_session, mocked_prompt_input, mocked_view_all_controller
):
    # Fill title
    title = "Buy milk"
    mocked_prompt_input.send_text(title)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Fill status by pressing down once
    status = 1
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Fill category name
    category_name = "personal"
    mocked_prompt_input.send_text(category_name)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Fill details
    # Move down and enter to select the "yes" option
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])
    details = "# Why I need to buy milk in markdown"
    mocked_prompt_input.send_text(details)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Esc>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        add_controller()

    assert Task.select().count() == 1, "One task has been created"
    assert Category.select().count() == 1, "One category has been created"

    task = Task.select().first()

    assert task.title == title
    assert task.status == status
    assert task.category.name == category_name
    assert task.details == details

    # In the end, we call the view all tasks again
    mocked_view_all_controller.assert_called_once()


def test_add_controller__no_category(
    tmp_db, mock_app_session, mocked_prompt_input, mocked_view_all_controller
):
    # Fill title
    title = "Buy milk"
    mocked_prompt_input.send_text(title)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Fill status by pressing down once
    status = 1
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Fill no category name by just pressing ENTER
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Fill details
    # Move down and enter to select the "yes" option
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])
    details = "# Why I need to buy milk in markdown"
    mocked_prompt_input.send_text(details)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Esc>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        add_controller()

    assert Task.select().count() == 1, "One task has been created"
    assert Category.select().count() == 0, "No category has been created"

    task = Task.select().first()

    assert task.title == title
    assert task.status == status
    assert task.category is None
    assert task.details == details

    # In the end, we call the view all tasks again
    mocked_view_all_controller.assert_called_once()
