from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_core.db import get_session

from .exception import NoteNotFound
from .repository import NoteRepository
from .schema import NoteCreate, NoteResponse, NoteUpdate
from .service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]


def get_note_service(
    session: SessionDep,
) -> NoteService:
    repository = NoteRepository(session)

    return NoteService(
        repository=repository,
        session=session,
    )


NoteServiceDep = Annotated[
    NoteService,
    Depends(get_note_service),
]


@router.get(
    "",
    response_model=list[NoteResponse],
)
async def list_notes(
    service: NoteServiceDep,
    q: str | None = None,
) -> list[NoteResponse]:
    return await service.list_notes(q)


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
async def get_note(
    note_id: int,
    service: NoteServiceDep,
) -> NoteResponse:
    try:
        return await service.get_note(note_id)
    except NoteNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    payload: NoteCreate,
    service: NoteServiceDep,
) -> NoteResponse:
    return await service.create_note(payload)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    service: NoteServiceDep,
) -> NoteResponse:
    try:
        return await service.update_note(note_id, payload)
    except NoteNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: int,
    service: NoteServiceDep,
) -> None:
    try:
        await service.delete_note(note_id)
    except NoteNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
