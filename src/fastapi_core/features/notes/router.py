from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from .exception import NoteNotFound
from .schema import NoteCreate, NoteResponse, NoteUpdate
from .service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


def get_note_service(request: Request) -> NoteService:
    return request.app.state.note_service


NoteServiceDep = Annotated[
    NoteService,
    Depends(get_note_service),
]


@router.get(
    "",
    response_model=list[NoteResponse],
)
def list_notes(
    service: NoteServiceDep,
    q: str | None = None,
) -> list[NoteResponse]:
    try:
        return service.list_notes(q)
    except NoteNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
def get_note(
    note_id: int,
    service: NoteServiceDep,
) -> NoteResponse:
    try:
        return service.get_note(note_id)
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
def create_note(
    payload: NoteCreate,
    service: NoteServiceDep,
) -> NoteResponse:
    return service.create_note(payload)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_id: int,
    payload: NoteUpdate,
    service: NoteServiceDep,
) -> NoteResponse:
    try:
        return service.update_note(note_id, payload)
    except NoteNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    service: NoteServiceDep,
) -> None:
    try:
        service.delete_note(note_id)
    except NoteNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
