from fastapi import APIRouter, Depends, Request, status

from .schema import NoteCreate, NoteResponse, NoteUpdate
from .service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


def get_note_service(request: Request) -> NoteService:
    return request.app.state.note_service


@router.get(
    "",
    response_model=list[NoteResponse],
)
def list_notes(
    q: str | None = None,
    service: NoteService = Depends(get_note_service),
) -> list[NoteResponse]:
    return service.list_notes(q)


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
def get_note(
    note_id: int,
    service: NoteService = Depends(get_note_service),
) -> NoteResponse:
    return service.get_note(note_id)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    payload: NoteCreate,
    service: NoteService = Depends(get_note_service),
) -> NoteResponse:
    return service.create_note(payload)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_id: int,
    payload: NoteUpdate,
    service: NoteService = Depends(get_note_service),
) -> NoteResponse:
    return service.update_note(note_id, payload)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    service: NoteService = Depends(get_note_service),
) -> None:
    service.delete_note(note_id)
