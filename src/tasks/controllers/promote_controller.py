from src.tasks.models.task import Task


def promote_controller(task_ids: list[int]) -> None:
    """Move up the status of selected todos"""
    Task.promote(task_ids)

    # TODO: call the `list_view` here at the end
