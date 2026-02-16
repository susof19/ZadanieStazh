"""Эндпоинты API рецептов."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Optional

if TYPE_CHECKING:
    from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import SessionLocal

router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_db() -> Generator[Session, None, None]:
    """Предоставляет сессию БД для запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DependsDb = Annotated[Session, Depends(get_db)]
QueryTag = Annotated[Optional[str], Query()]
QueryIngredient = Annotated[Optional[str], Query()]
QueryQ = Annotated[Optional[str], Query()]


@router.post("/", response_model=schemas.RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe_endpoint(
    recipe_in: schemas.RecipeCreate,
    db: DependsDb,
) -> schemas.RecipeOut:
    """Создать новый рецепт."""
    return crud.create_recipe(db, recipe_in)


@router.get("/", response_model=list[schemas.RecipeOut])
def list_recipes_endpoint(
    db: DependsDb,
    tag: QueryTag = None,
    ingredient: QueryIngredient = None,
    q: QueryQ = None,
) -> list[schemas.RecipeOut]:
    """Список рецептов с опциональной фильтрацией по тегу, ингредиенту или общему поиску."""
    recipes = crud.list_recipes(db, tag=tag, ingredient=ingredient, q=q)
    return [schemas.RecipeOut.model_validate(r) for r in recipes]


@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe_endpoint(
    recipe_id: int,
    db: DependsDb,
) -> schemas.RecipeOut:
    """Получить рецепт по id."""
    db_obj = crud.get_recipe(db, recipe_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    return db_obj


@router.put("/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe_endpoint(
    recipe_id: int,
    recipe_in: schemas.RecipeUpdate,
    db: DependsDb,
) -> schemas.RecipeOut:
    """Обновить рецепт по id."""
    db_obj = crud.get_recipe(db, recipe_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    return crud.update_recipe(db, db_obj, recipe_in)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_endpoint(
    recipe_id: int,
    db: DependsDb,
) -> None:
    """Удалить рецепт по id."""
    db_obj = crud.get_recipe(db, recipe_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    crud.delete_recipe(db, db_obj)
