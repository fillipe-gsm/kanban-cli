from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console, Group
from rich.layout import Layout
from rich.markup import escape
from rich.panel import Panel
from rich.rule import Rule

from config import settings

if TYPE_CHECKING:
    from src.tasks.models.task import Task


class ViewAllPresenter:
    """A class to display a summary list of tasks"""

    NO_CATEGORY_STR = "<No category>"

    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console()

    def present(self, tasks_by_status: dict[str, Task]) -> None:
        """Display a table-like view with all existing tasks

        The tasks are grouped by status, each one in a column.
        """
        layout = Layout(name="root")

        tasks_list = [
            self._present_tasks_in_status(tasks_by_status[status_id])
            for status_id, _ in enumerate(settings.statuses)
        ]
        layout.split_row(
            *(
                Layout(Panel(tasks, title=status))
                for tasks, status in zip(tasks_list, settings.statuses)
            )
        )

        self._console.print("\n")
        self._console.print(layout)

    def _present_tasks_in_status(self, tasks: list[Task]) -> str:
        """Writes a list of tasks in a status column

        The tasks should be presented like:

        <task1_display>
        ---
        <task2_display>
        ---
        <task3_display>
        ...
        """
        group_content = [
            el for task in tasks for el in (self._present_task(task), Rule())
        ]
        group_content.pop()  # remove last `Rule`

        return Group(*group_content)

    def _present_task(self, task: Task) -> str:
        """Display a single task

        Writes a task in the format:

            #<task_id> [<task_category>]
            <task_title>
        """
        category_str = (
            f"[{task.category.name}]"
            if task.category
            else f"[{self.NO_CATEGORY_STR}]"
        )

        return f"#{task.id} [bold]{escape(category_str)}[/bold]\n{task.title}"
