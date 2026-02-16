"""Точка входа приложения FastAPI."""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import recipes
from app.db import session as db_session
from app.db.base import Base

app = FastAPI(title="Recipes API")

Base.metadata.create_all(bind=db_session.engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root() -> FileResponse:
    """Отдача главной страницы."""
    return FileResponse("app/static/index.html")


app.include_router(recipes.router, prefix="/api/v1")
