from unittest.mock import patch

import pytest

from kanban_cli.categories.controllers.delete_controller import delete_controller
from kanban_cli.categories.models.category import Category
from kanban_cli.categories.presenters.cannot_delete_category_presenter import (
    CannotDeleteCategoryPresenter,
)
from kanban_cli.categories.presenters.no_category_presenter import NoCategoryPresenter
from kanban_cli.tasks.models.task import Task
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


@pytest.fixture
def mocked_no_category_presenter():
    with patch.object(NoCategoryPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_cannot_delete_category_presenter():
    with patch.object(CannotDeleteCategoryPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_view_all_controller():
    with patch(
        "src.categories.controllers.delete_controller.view_all_controller"
    ) as m:
        yield m


def test_no_categories_exist(
    tmp_db,
    mocked_no_category_presenter,
    mocked_view_all_controller,
):
    """
    As no category exist, we should see the appropriate message and not delete
    anything
    """
    category = Category.create(name="category")

    assert Category.select().count() == 1, "Sanity check: one task exists"

    delete_controller(category_id=category.id + 1)  # calls non-existing id
    assert Category.select().count() == 1, (
        "sanity check: the category still exists"
    )

    mocked_no_category_presenter.assert_called_once()
    mocked_view_all_controller.assert_not_called()


def test_category_exists_and_is_not_deleted(
    tmp_db,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    category = Category.create(name="category")
    assert Category.select().count() == 1, "Sanity check: one category exists"

    # Press Enter directly to select "no"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        delete_controller(category_id=category.id)

    assert Category.select().count() == 1, "category should still exist"

    mocked_view_all_controller.assert_called_once()


def test_category_with_linked_tasks_cannot_be_deleted(
    tmp_db,
    mocked_cannot_delete_category_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    category = Category.create(name="category")
    Task.create(title="buy milk", category=category)
    assert Category.select().count() == 1, "Sanity check: one category exists"

    # Press down once to select "yes"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        delete_controller(category_id=category.id)

    assert Category.select().count() == 1, "category still exists"

    # Also, only the view presenters is called to confirm the deletion
    mocked_cannot_delete_category_presenter.assert_called_once()


def test_category_without_linked_tasks_can_be_deleted(
    tmp_db,
    mocked_cannot_delete_category_presenter,
    mocked_view_all_controller,
    mocked_prompt_input,
    mock_app_session,
):
    category = Category.create(name="category")
    assert Category.select().count() == 1, "Sanity check: one category exists"

    # Press down once to select "yes"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        delete_controller(category_id=category.id)

    assert Category.select().count() == 0, "category got deleted"

    # Also, only the view presenters is called to confirm the deletion
    mocked_cannot_delete_category_presenter.assert_not_called()
    mocked_view_all_controller.assert_called_once()
