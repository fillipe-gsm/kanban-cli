from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt as prompt0
from pygments.lexers.markup import MarkdownLexer

from src.tasks.prompts.confirm_prompt import ConfirmPrompt

DETAILS_PROMPT_CHAR = "> "


class DetailsPrompt:
    def prompt(self) -> str:
        should_add_details_prompt = ConfirmPrompt(
            message="Do you want to add details? "
        )
        if not should_add_details_prompt.prompt():
            return ""

        return prompt0(
            DETAILS_PROMPT_CHAR,
            multiline=True,
            lexer=PygmentsLexer(MarkdownLexer),
            bottom_toolbar=self._bottom_toolbar,
            prompt_continuation=self._prompt_continuation,
        )

    @staticmethod
    def _bottom_toolbar() -> str:
        return (
            "Write details in markdown style. "
            "Type Alt+Enter or Esc+Enter when done."
        )

    @staticmethod
    def _prompt_continuation(
        width: int, line_number: int, is_soft_wrap: bool
    ) -> str:
        return DETAILS_PROMPT_CHAR
