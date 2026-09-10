from fastapi import HTTPException, status

# ERROR: you already moved Note schemas into features/notes/schema.py
# from fastapi_core.schemas import NoteCreate, NoteResponse, NoteUpdate
from .schema import NoteCreate, NoteResponse, NoteUpdate


class NoteService:
    def __init__(self) -> None:
        self.notes: dict[int, dict[str, object]] = {}
        self.next_id = 1

    # IMPROVE: no await / I/O here, so async is unnecessary
    def list_notes(
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

    # IMPROVE: same reason, regular def is enough
    def get_note(self, note_id: int) -> NoteResponse:
        if note_id not in self.notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                # ERROR: your old version had "\n" at the end
                # detail=f"No note with {note_id}\n",
                detail=f"No note with {note_id}",
            )

        return NoteResponse.model_validate(self.notes[note_id])

    def create_note(self, payload: NoteCreate) -> NoteResponse:
        note: dict[str, object] = {
            "id": self.next_id,
            **payload.model_dump(),
            "internal_version": 1,
        }

        self.notes[self.next_id] = note
        self.next_id += 1

        return NoteResponse.model_validate(note)

    def update_note(
        self,
        note_id: int,
        payload: NoteUpdate,
    ) -> NoteResponse:
        if note_id not in self.notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                # ERROR: this was NOT an f-string:
                # detail="No note with {note_id}"
                detail=f"No note with {note_id}",
            )

        update_data = payload.model_dump(exclude_unset=True)
        self.notes[note_id].update(update_data)

        current_version = self.notes[note_id]["internal_version"]

        if not isinstance(current_version, int):
            raise RuntimeError("Invalid internal version")

        self.notes[note_id]["internal_version"] = current_version + 1

        return NoteResponse.model_validate(self.notes[note_id])

    def delete_note(self, note_id: int) -> None:
        if note_id not in self.notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                # ERROR: same bug here, missing f before the string
                # detail="No note with {note_id}"
                detail=f"No note with {note_id}",
            )

        del self.notes[note_id]
