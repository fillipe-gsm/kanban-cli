from unittest.mock import patch

import pytest

from src.categories.controllers.add_controller import add_controller
from src.categories.models.category import Category
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


@pytest.fixture
def mocked_view_all_controller():
    with patch(
        "src.categories.controllers.add_controller.view_all_controller"
    ) as m:
        yield m


def test_add_controller__nonempty_category(
    tmp_db, mock_app_session, mocked_prompt_input, mocked_view_all_controller
):
    # Fill category name
    category_name = "personal"
    mocked_prompt_input.send_text(category_name)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        add_controller()

    assert Category.select().count() == 1, "one category has been created"

    category = Category.select().first()
    assert category.name == category_name

    # In the end, we call the view all tasks again
    mocked_view_all_controller.assert_called_once()


def test_add_controller__no_category(
    tmp_db, mock_app_session, mocked_prompt_input, mocked_view_all_controller
):
    # Fill no category name by just pressing ENTER
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        add_controller()

    assert Category.select().count() == 0, "No category has been created"

    # In the end, we call the view all categories again
    mocked_view_all_controller.assert_called_once()


def test_add_controller__repeated_category(
    tmp_db, mock_app_session, mocked_prompt_input, mocked_view_all_controller
):
    # Start with an existing category
    category_name = "personal"
    Category.create(name=category_name)
    assert Category.select().count() == 1, "sanity check: one category exists"

    # Fill in the prompt the same one
    mocked_prompt_input.send_text(category_name)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        add_controller()

    assert Category.select().count() == 1, "no new category has been created"

    # In the end, we call the view all tasks again
    mocked_view_all_controller.assert_called_once()
