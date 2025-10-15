from __future__ import annotations

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
    def group_by_status() -> dict[str, list[Task]]:
        """List all existing tasks by status and sorted by creation date"""
        tasks = (
            Task.select()
            .join(
                Category,
                on=(Task.category == Category.id),
                join_type=pw.JOIN.LEFT_OUTER,
            )
            .order_by(Task.created_at)
        )

        tasks_by_status = {i: [] for i, _ in enumerate(settings.statuses)}
        for task in tasks:
            tasks_by_status[task.status].append(task)

        return tasks_by_status

    @staticmethod
    def add_from_prompt(
        title: str, status: int, category_name: str, details: str
    ) -> Task:
        category, _ = (
            Category.get_or_create(name=category_name)
            if category_name
            else (None, False)
        )
        return Task.create(
            title=title, status=status, category=category, details=details
        )

    @staticmethod
    def promote(task_ids: list[int]) -> None:
        """Move up task status, truncating at the highest one"""
        max_status_level = len(Task.STATUS_CHOICES) - 1

        query = Task.update(
            status=pw.fn.MIN(Task.status + 1, max_status_level)
        ).where(Task.id.in_(task_ids))

        query.execute()
