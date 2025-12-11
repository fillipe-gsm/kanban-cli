from kanban_cli.tasks.prompts.status_prompt import StatusPrompt
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


def test_prompt_status__first_option_by_defaut(
    mocked_prompt_input, mock_app_session
):
    prompt = StatusPrompt()

    # Just press <Enter> without selecting anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        status = prompt.prompt()

    assert status == 0, "It selects first status by default"


def test_prompt_status__can_change_status(
    mocked_prompt_input, mock_app_session
):
    prompt = StatusPrompt()

    # Press below arrow twice and then enter
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Down>"])
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        status = prompt.prompt()

    assert status == 2, "Picks third status option"


def test_prompt_status__default_value(mocked_prompt_input, mock_app_session):
    current_status = 2
    prompt = StatusPrompt(default_value=current_status)

    # Just press <Enter> without selecting anything
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        status = prompt.prompt()

    assert status == current_status, "Status has been unchanged"
