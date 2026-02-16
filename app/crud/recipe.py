from sqlalchemy.orm import Session
from app import schemas
from app.models import Recipe
from fastapi import HTTPException, status
from typing import List, Optional

def get_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def list_recipes(db: Session, tag: Optional[str] = None, ingredient: Optional[str] = None, q: Optional[str] = None) -> List[Recipe]:
    query = db.query(Recipe)
    results = query.all()
    if q:
        q_trim = q.strip().lower()
        if q_trim:
            results = [
                r for r in results
                if (r.tags and any(q_trim in (t or "").lower() for t in r.tags))
                or any(q_trim in (ing or "").lower() for ing in (r.ingredients or []))
            ]
    else:
        if tag:
            tag_lower = tag.lower()
            results = [r for r in results if r.tags and any(tag_lower in (t or "").lower() for t in r.tags)]
        if ingredient:
            ing_lower = ingredient.lower()
            results = [r for r in results if any(ing_lower in (i or "").lower() for i in r.ingredients)]
    return results

def create_recipe(db: Session, recipe_in: schemas.RecipeCreate) -> Recipe:
    db_obj = Recipe(
        title=recipe_in.title.strip(),
        ingredients=recipe_in.ingredients,
        steps=recipe_in.steps,
        tags=recipe_in.tags or [],
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_recipe(db: Session, db_obj: Recipe, recipe_in: schemas.RecipeUpdate) -> Recipe:
    if recipe_in.title is not None:
        db_obj.title = recipe_in.title.strip()
    if recipe_in.ingredients is not None:
        db_obj.ingredients = recipe_in.ingredients
    if recipe_in.steps is not None:
        db_obj.steps = recipe_in.steps
    if recipe_in.tags is not None:
        db_obj.tags = recipe_in.tags
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_recipe(db: Session, db_obj: Recipe):
    db.delete(db_obj)
    db.commit()
