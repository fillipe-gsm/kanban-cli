import peewee as pw

from config import settings
from src.app.models import BaseModel


class Category(BaseModel):
    name = pw.CharField(
        max_length=settings.category__name_max_length,
        constraints=[
            pw.Check(f"length(name) <= {settings.category__name_max_length}")
        ],
    )

    def __str__(self) -> str:
        return self.name
