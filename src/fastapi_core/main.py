from fastapi import FastAPI

from fastapi_core.routers.articles import router as articles_router
from fastapi_core.routers.notes import router as notes_router

app = FastAPI(
    title="FastAPI Core",
)

app.include_router(notes_router)
app.include_router(articles_router)
