import peewee as pw
import pytest

from kanban_cli.config import settings
from kanban_cli.categories.models.category import Category


def test_can_create_valid_category(tmp_db):
    assert Category.select().count() == 0, "Sanity check: no categories yet"

    Category.create(name="personal")

    assert Category.select().count() == 1, "One category created"


def test_cannot_create_category_with_long_name(tmp_db):
    assert Category.select().count() == 0, "Sanity check: no categories yet"

    long_name = "a" * (settings.category__name_max_length + 1)

    with pytest.raises(pw.IntegrityError):
        Category.create(name=long_name)

    assert Category.select().count() == 0, "Sanity check: still no categories"


def test_cannot_create_repeated_categories(tmp_db):
    Category.create(name="category")  # works

    with pytest.raises(pw.IntegrityError):
        # Attempting to create repeated category fails
        Category.create(name="category")

    Category.create(name="other category")  # but can create new ones


def test_category_names(tmp_db):
    Category.create(name="category 1")
    Category.create(name="category 2")
    Category.create(name="category 3")

    expected_category_names = ["category 1", "category 2", "category 3"]

    assert Category.category_names() == expected_category_names


def test_edit_from_prompt(tmp_db):
    category = Category.create(name="perssonal")
    assert Category.select().count() == 1, "sanity check: one category exists"

    new_category_name = "personal"
    category.edit_from_prompt(category_name=new_category_name)

    assert Category.select().count() == 1, "no new category got created"
    assert Category.get_by_id(pk=category.id).name == new_category_name, (
        "category name got updated"
    )
