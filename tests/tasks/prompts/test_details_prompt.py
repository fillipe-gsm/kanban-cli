from src.tasks.prompts.details_prompt import DetailsPrompt
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


def test_dont_add_details_by_default(mocked_prompt_input, mock_app_session):
    prompt = DetailsPrompt()

    # Press Enter without selecting anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        details = prompt.prompt()

    assert details == "", "No details are added by default"


def test_can_add_details(mocked_prompt_input, mock_app_session):
    prompt = DetailsPrompt()

    # Move down and enter to select the "yes" option
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Type the details, and finish with Esc+Enter
    expected_details = "# Details in `markdown`"
    mocked_prompt_input.send_text(expected_details)
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Esc>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        details = prompt.prompt()

    assert details == expected_details, "We get expected details"


def test_edit__no_prompt_returns_default_value(
    mocked_prompt_input, mock_app_session
):
    current_details = "# Reasons to buy milk"
    prompt = DetailsPrompt(default_value=current_details, is_editing=True)

    # Press ENTER to not edit current details
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        new_details = prompt.prompt()

    assert new_details == current_details, "Details remain unchanged"


def test_edit__can_update_current_details(
    mocked_prompt_input, mock_app_session
):
    current_details = "# Reasons to buy milc"
    prompt = DetailsPrompt(default_value=current_details, is_editing=True)

    # Move down and enter to select the "yes" option
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    # Press backspace and type the extra characters
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Backspace>"])
    extra_details = "k (I fixed the typo)"
    mocked_prompt_input.send_text(extra_details)
    # Then, press Esc+Enter to accept
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Esc>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        new_details = prompt.prompt()

    assert new_details == "# Reasons to buy milk (I fixed the typo)", (
        "Details have been updated"
    )
