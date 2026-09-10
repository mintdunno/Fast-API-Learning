from fastapi import APIRouter, HTTPException, status

from fastapi_core.features.notes.service import NoteService
from fastapi_core.schemas import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

service = NoteService()


@router.get(
    "",
    response_model=list[NoteResponse],
)
service.list_notes()

@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
async def get_note(
    note_id: int,
) -> NoteResponse:
    if note_id not in notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return NoteResponse.model_validate(notes[note_id])


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    payload: NoteCreate,
) -> NoteResponse:
    global next_id

    note: dict[str, object] = {
        "id": next_id,
        **payload.model_dump(),
        "internal_version": 1,
    }

    notes[next_id] = note
    next_id += 1

    return NoteResponse.model_validate(note)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
) -> NoteResponse:
    if note_id not in notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    update_data = payload.model_dump(
        exclude_unset=True,
    )

    notes[note_id].update(update_data)

    current_version = notes[note_id]["internal_version"]

    if not isinstance(current_version, int):
        raise RuntimeError("Invalid internal version")

    notes[note_id]["internal_version"] = current_version + 1

    return NoteResponse.model_validate(notes[note_id])


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: int,
) -> None:
    if note_id not in notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    del notes[note_id]
