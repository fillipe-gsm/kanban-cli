from typing import Annotated

from typer import Option, Typer

from config import settings
from src.app.models import db
from src.tasks.controllers.add_controller import add_controller
from src.tasks.controllers.delete_controller import delete_controller
from src.tasks.controllers.edit_controller import edit_controller
from src.tasks.controllers.promote_controller import promote_controller
from src.tasks.controllers.regress_controller import regress_controller
from src.tasks.controllers.view_all_controller import view_all_controller
from src.tasks.controllers.view_controller import view_controller


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

    @app.command()
    def view_all() -> None:
        """List all existing tasks in a tabular format"""
        view_all_controller()

    @app.command()
    def view(task_id: int) -> None:
        """Show a specific task with full details"""
        view_controller(task_id)

    @app.command()
    def add() -> None:
        """Add a new task"""
        add_controller()

    @app.command()
    def edit(task_id: int) -> None:
        """Edit an existing task"""
        edit_controller(task_id)

    @app.command()
    def delete(task_id: int) -> None:
        """Delete a task forever"""
        delete_controller(task_id)

    @app.command()
    def promote(task_ids: list[int]) -> None:
        """Move a list of tasks one status up

        \b
        Tasks at the highest status are kept at this level.
        Also, non-existing tasks are skipped.
        """
        promote_controller(task_ids)

    @app.command()
    def regress(task_ids: list[int]) -> None:
        """Move a list of tasks one status down

        \b
        Tasks at the lowest status are kept at this level.
        Also, non-existing tasks are skipped.
        """
        regress_controller(task_ids)

    return app
