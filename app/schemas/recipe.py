from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1)
    ingredients: List[str]
    steps: List[str]
    tags: Optional[List[str]] = []

    @validator("ingredients", "steps")
    def non_empty_list(cls, v):
        if not v or any(not isinstance(item, str) or not item.strip() for item in v):
            raise ValueError("ввод должен быть не пустым списком строк или не пустыми строками")
        return v

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    ingredients: Optional[List[str]] = None
    steps: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    @validator("ingredients", "steps")
    def non_empty_if_provided(cls, v):
        if v is not None:
            if not v or any(not isinstance(item, str) or not item.strip() for item in v):
                raise ValueError("ввод должен быть не пустым списком строк или не пустыми строками")
        return v

class RecipeOut(RecipeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
