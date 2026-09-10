from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_core.config import settings
from fastapi_core.features.notes.router import router as notes_router
from fastapi_core.features.notes.service import NoteService
from fastapi_core.routers.articles import router as articles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.note_service = NoteService()

    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(notes_router)
app.include_router(articles_router)
