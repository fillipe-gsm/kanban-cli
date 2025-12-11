from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from kanban_cli.app.app import create_app

runner = CliRunner()


@pytest.fixture
def tst_app():
    return create_app()


def test_view_all(tst_app, tmp_db):
    with patch("src.categories.categories_app.view_all_controller") as m:
        runner.invoke(tst_app, ["categories", "view-all"])

    # Add controller was called
    m.assert_called_once()


def test_add(tst_app, tmp_db):
    with patch("src.categories.categories_app.add_controller") as m:
        runner.invoke(tst_app, ["categories", "add"])

    # Add controller was called
    m.assert_called_once()


def test_edit(tst_app, tmp_db):
    category_id = 1
    with patch("src.categories.categories_app.edit_controller") as m:
        runner.invoke(tst_app, ["categories", "edit", f"{category_id}"])

    # Add controller was called with proper id
    m.assert_called_once_with(category_id)


def test_delete(tst_app, tmp_db):
    category_id = 1
    with patch("src.categories.categories_app.delete_controller") as m:
        runner.invoke(tst_app, ["categories", "delete", f"{category_id}"])

    # Add controller was called with proper id
    m.assert_called_once_with(category_id)
