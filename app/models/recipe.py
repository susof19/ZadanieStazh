from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import JSON
from datetime import datetime, timezone
from app.db.base import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    ingredients = Column(JSON, nullable=False)  # список строк
    steps = Column(JSON, nullable=False)        # список строк
    tags = Column(JSON, nullable=True)          # опционально
    created_at = Column(
        DateTime,
        default=lambda: datetime.utcnow(),
        nullable=False
    )
