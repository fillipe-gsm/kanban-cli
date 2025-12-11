from kanban_cli.tasks.prompts.priority_prompt import PriorityPrompt
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


def test_prompt_priority__middle_option_by_defaut(
    mocked_prompt_input, mock_app_session
):
    prompt = PriorityPrompt()

    # Just press <Enter> without selecting anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        priority = prompt.prompt()

    assert priority == 2, "It selects middle priority by default"


def test_prompt_priority__can_change_priority(
    mocked_prompt_input, mock_app_session
):
    prompt = PriorityPrompt()

    # Press below arrow twice and then enter
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        priority = prompt.prompt()

    assert priority == 4, "Picks fifth priority option"


def test_prompt_priority__existing_value(
    mocked_prompt_input, mock_app_session
):
    current_priority = 0
    prompt = PriorityPrompt(default_value=current_priority)

    # Just press <Enter> without selecting anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        priority = prompt.prompt()

    assert priority == current_priority, "priority has been unchanged"
