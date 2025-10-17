from src.tasks.controllers.view_all_controller import view_all_controller
from src.tasks.controllers.view_controller import view_controller
from src.tasks.models.task import Task
from src.tasks.presenters.no_task_presenter import NoTaskPresenter
from src.tasks.prompts.confirm_prompt import ConfirmPrompt


def delete_controller(task_id: int) -> None:
    """Delete a task via its id"""
    task: Task = Task.get_or_none(Task.id == task_id)
    if not task:
        NoTaskPresenter().present(task_id=task_id)
        return

    view_controller(task_id)
    if ConfirmPrompt(
        message=f"Confirm deletion of task #{task.id}? "
    ).prompt():
        task.delete_instance()

    view_all_controller()
