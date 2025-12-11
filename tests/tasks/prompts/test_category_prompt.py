from kanban_cli.categories.models.category import Category
from kanban_cli.tasks.prompts.category_prompt import CategoryPrompt
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


def test_category_prompt__can_write_other_category(
    mocked_prompt_input, mock_app_session, tmp_db
):
    Category.create(name="category 1")
    Category.create(name="category 2")
    Category.create(name="category 3")

    prompt = CategoryPrompt(category_names=Category.category_names())

    other_category_str = "other category"
    mocked_prompt_input.send_text(other_category_str)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])
    with mock_app_session:
        category_name = prompt.prompt()

    assert category_name == other_category_str, (
        "Can input non-existing category"
    )


def test_category_prompt__can_write_empty_category(
    mocked_prompt_input, mock_app_session
):
    prompt = CategoryPrompt()

    # Press ENTER without writing anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])
    with mock_app_session:
        category_name = prompt.prompt()

    assert category_name == "", "Can input empty category"


def test_selected_default_value(tmp_db, mocked_prompt_input, mock_app_session):
    category1 = Category.create(name="category 1")
    Category.create(name="category 2")
    Category.create(name="category 3")

    prompt = CategoryPrompt(
        default_value=category1.name, category_names=Category.category_names()
    )

    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])
    with mock_app_session:
        new_category_name = prompt.prompt()

    assert new_category_name == category1.name, "Category remains unchanged"


def test_can_change_default_value(
    tmp_db, mocked_prompt_input, mock_app_session
):
    category1 = Category.create(name="category 1")
    Category.create(name="category 2")
    Category.create(name="category 3")

    prompt = CategoryPrompt(
        default_value=category1.name, category_names=Category.category_names()
    )

    mocked_prompt_input.send_text(KEY_MAPPINGS["<Backspace>"])
    mocked_prompt_input.send_text("4")  # replace to `category 4`
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])
    with mock_app_session:
        new_category_name = prompt.prompt()

    assert new_category_name == "category 4", "Category got changed"
