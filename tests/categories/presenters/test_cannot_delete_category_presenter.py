from io import StringIO

from rich.console import Console

from src.categories.presenters.cannot_delete_category_presenter import (
    CannotDeleteCategoryPresenter,
)


def test_cannot_delete_category_presenter():
    category_name = "personal"
    linked_task_ids = [1, 2, 5]

    console = Console(file=StringIO())
    presenter = CannotDeleteCategoryPresenter(console=console)
    presenter.present(category_name, linked_task_ids)

    console_output = console.file.getvalue()  # ty: ignore[unresolved-attribute]
    assert category_name in console_output, "category name is in output"
    for task_id in linked_task_ids:
        assert str(task_id) in console_output, "task id is in output"
