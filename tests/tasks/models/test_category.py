import peewee as pw
import pytest

from config import settings
from src.tasks.models.category import Category


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
