from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db.session import SessionLocal

router = APIRouter(prefix="/recipes", tags=["recipes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe_endpoint(recipe_in: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe_in)

@router.get("/", response_model=List[schemas.RecipeOut])
def list_recipes_endpoint(tag: Optional[str] = Query(None), ingredient: Optional[str] = Query(None), q: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return crud.list_recipes(db, tag=tag, ingredient=ingredient, q=q)

@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_recipe(db, recipe_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return db_obj

@router.put("/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe_endpoint(recipe_id: int, recipe_in: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_obj = crud.get_recipe(db, recipe_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return crud.update_recipe(db, db_obj, recipe_in)

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_recipe(db, recipe_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    crud.delete_recipe(db, db_obj)
    return None
