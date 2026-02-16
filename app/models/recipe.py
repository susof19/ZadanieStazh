"""Модель рецепта SQLAlchemy."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.types import JSON

from app.db.base import Base


def _utc_now() -> datetime:
    """Текущее время UTC (для значения по умолчанию)."""
    return datetime.now(timezone.utc)


class Recipe(Base):
    """Таблица рецептов: название, ингредиенты, шаги, теги, дата создания."""

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    ingredients = Column(JSON, nullable=False)  # список строк
    steps = Column(JSON, nullable=False)  # список строк
    tags = Column(JSON, nullable=True)  # опционально
    created_at = Column(
        DateTime,
        default=_utc_now,
        nullable=False,
    )
