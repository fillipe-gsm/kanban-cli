import pytest

from config import settings
from kanban_cli.tasks.prompts.title_prompt import TitlePrompt
from tests.tasks.prompts.key_mappings import KEY_MAPPINGS


def test_prompt_title__valid(mocked_prompt_input, mock_app_session):
    """Check if we get the proper title if it is valid"""
    prompt = TitlePrompt()

    # We pass `\n` to indicate a RETURN press
    expected_title = "buy milk"
    mocked_prompt_input.send_text(f"{expected_title}\n")

    with mock_app_session:
        title = prompt.prompt()

    assert title == expected_title


def test_prompt_title__empty_prompt(mocked_prompt_input, mock_app_session):
    """Test that we cannot receive an empty prompt

    The way of testing this is not very good, but it is the best I could find.
    If we pass an input that fails the validator, it simply won't let
    the prompt be closed. So, in a test, after `mocked_prompt_input.send_text`,
    it simply hangs waiting for a valid input.

    To test for that, I force closing the prompt, and in this case we should
    receive an `EOFError` as nothing has been passed.

    This unfortunately does not test the validation error per se, but it
    ensures that the input is recognized as invalid, so it is the best I could
    get.
    """
    prompt = TitlePrompt()

    mocked_prompt_input.send_text("\n")
    mocked_prompt_input.close()  # force closing the prompt right after

    with mock_app_session, pytest.raises(EOFError):
        prompt.prompt()


def test_prompt_title__too_large_prompt(mocked_prompt_input, mock_app_session):
    prompt = TitlePrompt()

    too_long_title = "a" * (settings.task__title_max_length + 1)
    mocked_prompt_input.send_text(f"{too_long_title}\n")
    mocked_prompt_input.close()  # force closing the prompt right after

    with mock_app_session, pytest.raises(EOFError):
        prompt.prompt()


def test_prompt_title__default_value(mocked_prompt_input, mock_app_session):
    current_title = "buy milk"
    prompt = TitlePrompt(default_value=current_title)

    # Just accept the default value
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        title = prompt.prompt()

    assert title == current_title, "Title remains unchanged"


def test_prompt_title__can_update_default_value(
    mocked_prompt_input, mock_app_session
):
    current_title = "buy milc"
    prompt = TitlePrompt(default_value=current_title)

    # Press backspace and fix last character with "k"
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Backspace>"])
    mocked_prompt_input.send_text("k")
    mocked_prompt_input.send_text(KEY_MAPPINGS["<Enter>"])

    with mock_app_session:
        title = prompt.prompt()

    assert title == "buy milk", "Title has been fixed"
