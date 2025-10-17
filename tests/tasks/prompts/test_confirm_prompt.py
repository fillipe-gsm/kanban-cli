from src.tasks.prompts.confirm_prompt import ConfirmPrompt
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


def test_default(mocked_prompt_input, mock_app_session):
    """Check it returns `False` by default"""
    prompt = ConfirmPrompt(message="Will it return `False`? ")

    # Press Enter without selecting anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        flag = prompt.prompt()

    assert flag is False, "Returns `False` by default"


def test_can_select_yes(mocked_prompt_input, mock_app_session):
    prompt = ConfirmPrompt(message="Will it return `True`? ")

    # Move down and enter to select the "yes" option
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        flag = prompt.prompt()

    assert flag is True, "Returns `True` when selecting yes"
