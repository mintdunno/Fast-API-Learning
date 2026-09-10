from fastapi import APIRouter, status

from .schema import NoteCreate, NoteResponse, NoteUpdate
from .service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

service = NoteService()


@router.get(
    "",
    response_model=list[NoteResponse],
)
def list_notes(
    q: str | None = None,
) -> list[NoteResponse]:
    return service.list_notes(q)


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
def get_note(
    note_id: int,
) -> NoteResponse:
    return service.get_note(note_id)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    payload: NoteCreate,
) -> NoteResponse:
    return service.create_note(payload)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_id: int,
    payload: NoteUpdate,
) -> NoteResponse:
    return service.update_note(note_id, payload)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
) -> None:
    service.delete_note(note_id)
