from fastapi import HTTPException, status

from fastapi_core.schemas import NoteCreate, NoteResponse, NoteUpdate


class NoteService:
    def __init__(self) -> None:
        self.notes: dict[int, dict[str, object]] = {}
        self.next_id = 1

    async def list_notes(
        self,
        q: str | None = None,
    ) -> list[NoteResponse]:
        if q is None:
            return [NoteResponse.model_validate(note) for note in self.notes.values()]

        return [
            NoteResponse.model_validate(note)
            for note in self.notes.values()
            if q.lower() in str(note["title"]).lower()
        ]

    async def get_note(self, note_id: int) -> NoteResponse:
        if note_id not in self.notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No note with {note_id}\n",
            )

        return NoteResponse.model_validate(self.notes[note_id])

    async def create_note(self, payload: NoteCreate) -> NoteResponse:
        note: dict[str, object] = {
            "id": self.next_id,
            **payload.model_dump(),
            "internal_version": 1,
        }

        self.notes[self.next_id] = note
        self.next_id += 1

        return NoteResponse.model_validate(note)

    async def update_note(self, note_id: int, payload: NoteUpdate) -> NoteResponse:
        if note_id not in self.notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No note with {note_id}"
            )
        update_data = payload.model_dump(exclude_unset=True)
        self.notes[note_id].update(update_data)
        current_version = self.notes[note_id]["internal_version"]

        if not isinstance(current_version, int):
            raise RuntimeError("Invalid internal version")  # noqa: TRY004

        self.notes[note_id]["internal_version"] = current_version + 1

        return NoteResponse.model_validate(self.notes[note_id])

    async def delete_note(self, note_id: int) -> None:
        if note_id not in self.notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No note with {note_id}"
            )

        del self.notes[note_id]
