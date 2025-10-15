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
