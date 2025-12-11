from unittest.mock import patch

import pytest

from kanban_cli.categories.controllers.edit_controller import edit_controller
from kanban_cli.categories.models.category import Category
from kanban_cli.categories.presenters.no_category_presenter import NoCategoryPresenter
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


@pytest.fixture
def mocked_view_all_controller():
    with patch(
        "kanban_cli.categories.controllers.edit_controller.view_all_controller"
    ) as m:
        yield m


@pytest.fixture
def mocked_no_category_presenter():
    with patch.object(NoCategoryPresenter, "present") as m:
        yield m


def test_no_categories_exist(
    tmp_db, mocked_no_category_presenter, mocked_view_all_controller
):
    """As no categories exist, we should see the appropriate message"""
    edit_controller(category_id=1)

    mocked_no_category_presenter.assert_called_once()
    mocked_view_all_controller.assert_not_called()


def test_edit_defaults(
    tmp_db,
    mocked_no_category_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    """Test we get an updated task with no changes"""
    category = Category.create(name="category")
    assert Category.select().count() == 1, "sanity check: one category exists"

    # Just press enter to accept existing category
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        edit_controller(category_id=category.id)

    edited_category = Category.get_by_id(pk=category.id)

    # Sanity check: no property got changed
    assert category.name == edited_category.name
    assert Category.select().count() == 1, (
        "sanity check: no new category was created"
    )


def test_edit_defaults__can_update_attribute(
    tmp_db,
    mocked_no_category_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    category = Category.create(name="categori")
    assert Category.select().count() == 1, "sanity check: one category exists"

    # Press backspace to fix the typo and add the correct character
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Backspace>"])
    mocked_prompt_input.send_text("y")
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        edit_controller(category_id=category.id)

    edited_category = Category.get_by_id(pk=category.id)

    assert edited_category.name == "category", (
        "category should have been fixed to no typo"
    )
    assert Category.select().count() == 1, (
        "sanity check: no new category was created"
    )
