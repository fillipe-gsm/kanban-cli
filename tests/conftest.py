from collections.abc import Iterator

import peewee as pw
import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.shortcuts.prompt import PromptSession

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


@pytest.fixture
def mocked_prompt_input():
    with create_pipe_input() as inp:
        yield inp


@pytest.fixture
def mock_app_session(mocked_prompt_input):
    """Returns a context manager that can be used to mock a call to a prompt"""
    return create_app_session(input=mocked_prompt_input, output=DummyOutput())
