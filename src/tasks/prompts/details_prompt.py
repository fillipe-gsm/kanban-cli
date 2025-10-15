from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.shortcuts import prompt as prompt0
from pygments.lexers.markup import MarkdownLexer

YES_PROMPT = "y"
NO_PROMPT = "n"
DETAILS_PROMPT_CHAR = "> "


class DetailsPrompt:
    def prompt(self) -> str:
        yes_or_no = [(NO_PROMPT, "No"), (YES_PROMPT, "Yes")]
        flag = choice(
            message="Do you want to add details? ",
            options=yes_or_no,
            default=NO_PROMPT,
        )

        if flag == NO_PROMPT:
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
