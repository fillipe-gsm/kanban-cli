from prompt_toolkit.shortcuts import choice

from config import settings


class StatusPrompt:
    """Select among possible status"""

    def prompt(self) -> int:
        options = [(i, status) for i, status in enumerate(settings.statuses)]
        return choice(message="Status: ", options=options, default=0)
