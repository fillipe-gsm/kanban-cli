from collections.abc import Iterator

import peewee as pw
import pytest

from src.tasks.models.category import Category
from src.tasks.models.task import Task

TEST_DB = pw.SqliteDatabase(":memory:")
MODELS = [Category, Task]


@pytest.fixture
def tmp_db() -> Iterator[pw.SqliteDatabase]:
    TEST_DB.bind(MODELS)
    TEST_DB.connect()
    TEST_DB.create_tables(models=MODELS)

    yield TEST_DB

    TEST_DB.drop_tables(models=MODELS)
    TEST_DB.close()
