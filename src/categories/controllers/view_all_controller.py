from src.categories.models.category import Category
from src.categories.presenters.no_categories_presenter import (
    NoCategoriesPresenter,
)
from src.categories.presenters.view_all_presenter import ViewAllPresenter


def view_all_controller() -> None:
    """Query and list all existing categories, if any"""
    # Efficient test if any category exists
    if Category.select().limit(1).exists() == 0:
        NoCategoriesPresenter().present()
        return

    ViewAllPresenter().present(categories=Category.list_categories())
