from datetime import datetime

import peewee as pw

from config import settings
from src.app.models import BaseModel
from src.tasks.models.category import Category


class Task(BaseModel):
    STATUS_CHOICES = [(i, val) for i, val in enumerate(settings.statuses)]
    _allowed_statuses = ", ".join(str(i) for i, _ in STATUS_CHOICES)

    title = pw.CharField(
        max_length=settings.task__title_max_length,
        constraints=[
            pw.Check(f"length(title) <= {settings.task__title_max_length}")
        ],
    )
    status = pw.IntegerField(
        choices=STATUS_CHOICES,
        default=0,  # first status by default
        constraints=[pw.Check(f"status IN ({_allowed_statuses})")],
    )
    category = pw.ForeignKeyField(Category, backref="tasks", null=True)
    created_at = pw.DateTimeField(default=datetime.now())
    details = pw.TextField(null=True)

    def __str__(self) -> str:
        return (
            f"Title: {self.title}; "
            f"Status: {self.status_str}; "
            f"Category: {self.category}; "
            f"Created at: {self.created_at_str}"
        )

    @property
    def status_str(self) -> str:
        """Human-readable visualization of status"""
        return settings.statuses[self.status]

    @property
    def created_at_str(self) -> str:
        """Human-readable visualization of creation date"""
        return self.created_at.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def promote(task_ids: list[int]) -> None:
        """Move up task status, truncating at the highest one"""
        max_status_level = len(Task.STATUS_CHOICES) - 1

        query = Task.update(
            status=pw.fn.MIN(Task.status + 1, max_status_level)
        ).where(Task.id.in_(task_ids))

        query.execute()
