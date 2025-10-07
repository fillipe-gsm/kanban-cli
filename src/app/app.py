from typing import Annotated

from typer import Option, Typer

from config import settings
from src.app.models import db
from src.tasks.views.promote_view import promote_view


def create_app() -> Typer:
    """Build a cli kanban app"""

    app = Typer()

    @app.callback()
    def main(
        filename: Annotated[
            str, Option("-f", "--filename", help="File name")
        ] = settings.default_db_name,
    ) -> None:
        """Simple Kanban management in the command line"""
        # Local import to prevent circular imports
        from src.tasks.models import MODELS  # noqa: E402

        db.init(filename)
        db.create_tables(MODELS)

    @app.command()
    def promote(task_ids: list[int]) -> None:
        """Move a list of tasks one status up

        \b
        Tasks at the highest status are kept at this level.
        Also, non-existing tasks are skipped.
        """
        promote_view(task_ids)

    @app.command()
    def view_all() -> None:
        """List all existing tasks"""

    return app
