from src.tasks.controllers.view_all_controller import view_all_controller
from src.tasks.models.task import Task


def regress_controller(task_ids: list[int]) -> None:
    """Move down the status of selected todos"""
    Task.regress(task_ids)

    # Print all tasks back
    view_all_controller()
