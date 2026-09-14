from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_core.config import settings
from fastapi_core.db import engine
from fastapi_core.features.articles.router import router as articles_router
from fastapi_core.features.articles.service import ArticleService
from fastapi_core.features.notes.router import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.article_service = ArticleService()

    yield

    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(notes_router)
app.include_router(articles_router)
