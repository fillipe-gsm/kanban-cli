from unittest.mock import patch

import pytest

from src.categories.controllers.view_all_controller import view_all_controller
from src.categories.models.category import Category
from src.categories.presenters.no_categories_presenter import (
    NoCategoriesPresenter,
)
from src.categories.presenters.view_all_presenter import ViewAllPresenter


@pytest.fixture
def mocked_no_categories_presenter():
    with patch.object(NoCategoriesPresenter, "present") as m:
        yield m


@pytest.fixture
def mocked_view_all_presenter():
    with patch.object(ViewAllPresenter, "present") as m:
        yield m


def test_no_categories_exist(
    tmp_db, mocked_no_categories_presenter, mocked_view_all_presenter
):
    view_all_controller()

    # As there are no categories, it calls the "no categories presenter"
    mocked_no_categories_presenter.assert_called_once()
    mocked_view_all_presenter.assert_not_called()


def test_categories_exist(
    tmp_db, mocked_no_categories_presenter, mocked_view_all_presenter
):
    Category.create(name="cat1")
    Category.create(name="cat2")

    view_all_controller()

    # As there are categories, it calls the "view all categories presenter"
    mocked_no_categories_presenter.assert_not_called()
    mocked_view_all_presenter.assert_called_once()
