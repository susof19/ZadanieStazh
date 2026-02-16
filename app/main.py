from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1 import recipes
from app.db import session as db_session
from app.db.base import Base
from app.models import recipe as recipe_model

app = FastAPI(title="Recipes API")

Base.metadata.create_all(bind=db_session.engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/")
def root():
    return FileResponse("app/static/index.html")
app.include_router(recipes.router, prefix="/api/v1")
