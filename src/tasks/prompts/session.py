from __future__ import annotations

from typing import TYPE_CHECKING

from prompt_toolkit.shortcuts import PromptSession

if TYPE_CHECKING:
    from prompt_toolkit.input import Input
    from prompt_toolkit.output import Output


def create_session(
    input_: Input | None = None, output: Output | None = None
) -> PromptSession:
    return PromptSession(input=input_, output=output)
