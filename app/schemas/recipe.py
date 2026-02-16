"""Схемы Pydantic для API рецептов.
"""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import List, Optional  # noqa: UP035

from pydantic import BaseModel, Field, field_validator

_ERR_NON_EMPTY = "ввод должен быть не пустым списком строк или не пустыми строками"


class RecipeBase(BaseModel):
    """Базовые поля рецепта: название, ингредиенты, шаги, теги."""

    title: str = Field(..., min_length=1)
    ingredients: List[str]  # noqa: UP006
    steps: List[str]  # noqa: UP006
    tags: Optional[List[str]] = []  # noqa: UP006, UP045

    @field_validator("ingredients", "steps")
    @classmethod
    def non_empty_list(cls, v: List[str]) -> List[str]:  # noqa: N805, UP006
        """Список не пуст и все элементы — непустые строки."""
        if not v or any(not isinstance(item, str) or not item.strip() for item in v):
            raise ValueError(_ERR_NON_EMPTY)
        return v


class RecipeCreate(RecipeBase):
    """Схема для создания рецепта."""


class RecipeUpdate(BaseModel):
    """Схема для частичного обновления рецепта."""

    title: Optional[str] = Field(None, min_length=1)  # noqa: UP045
    ingredients: Optional[List[str]] = None  # noqa: UP006, UP045
    steps: Optional[List[str]] = None  # noqa: UP006, UP045
    tags: Optional[List[str]] = None  # noqa: UP006, UP045

    @field_validator("ingredients", "steps")
    @classmethod
    def non_empty_if_provided(cls, v: Optional[List[str]]) -> Optional[List[str]]:  # noqa: N805, UP006, UP045
        """Если передано — список не пуст и элементы непустые строки."""
        if v is not None and (
            not v or any(not isinstance(item, str) or not item.strip() for item in v)
        ):
            raise ValueError(_ERR_NON_EMPTY)
        return v


class RecipeOut(RecipeBase):
    """Схема ответа с рецептом: id и дата создания."""

    id: int
    created_at: datetime

    class Config:
        """Настройка Pydantic для режима ORM."""

        from_attributes = True
