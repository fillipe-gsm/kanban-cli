from typing import Annotated

from typer import Option, Typer

from config import settings
from src.app.models import db
from src.categories.categories_app import create_app as create_categories_app
from src.tasks.tasks_app import create_app as create_tasks_app


def create_app() -> Typer:
    """Build a cli kanban app"""

    app = Typer()

    @app.callback()
    def main(
        filename: Annotated[
            str, Option("-f", "--filename", help="File name")
        ] = settings.db_name,
    ) -> None:
        """Simple Kanban management in the command line"""
        # Local import to prevent circular imports
        from src.tasks.models import MODELS  # noqa: E402

        db.init(filename)
        db.create_tables(MODELS)

    app.add_typer(create_tasks_app(), name="tasks")
    app.add_typer(create_categories_app(), name="categories")

    return app
