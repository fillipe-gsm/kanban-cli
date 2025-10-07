from typing import Annotated

from typer import Option, Typer

from config import settings
from src.app.models import db


def create_app() -> Typer:
    """Build a cli app"""

    app = Typer()

    @app.callback()
    def main(
        filename: Annotated[
            str, Option("-f", "--filename", help="File name")
        ] = settings.default_db_name,
    ) -> None:
        """Simple Kanban management in command line"""
        # Local import to prevent circular imports
        from src.tasks.models import MODELS  # noqa: E402

        db.init(filename)
        db.create_tables(MODELS)

    @app.command()
    def promote(task_id: str) -> None:
        """Do stuff"""
        pass

    return app
