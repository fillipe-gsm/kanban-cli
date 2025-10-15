from src.tasks.controllers.view_all_controller import view_all_controller
from src.tasks.models.category import Category
from src.tasks.models.task import Task
from src.tasks.prompts.category_prompt import CategoryPrompt
from src.tasks.prompts.details_prompt import DetailsPrompt
from src.tasks.prompts.status_prompt import StatusPrompt
from src.tasks.prompts.title_prompt import TitlePrompt


def add_controller() -> None:
    """Run a sequence of prompts to add a new task"""
    title = TitlePrompt().prompt()
    status = StatusPrompt().prompt()
    category_names = Category.category_names()
    category_name = CategoryPrompt(category_names=category_names).prompt()
    details = DetailsPrompt().prompt()

    Task.add_from_prompt(title, status, category_name, details)

    # Print all tasks back
    view_all_controller()
