from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_core.features.notes.exception import NoteNotFound
from fastapi_core.features.notes.model import Note

from .repository import NoteRepository

# ERROR: you already moved Note schemas into features/notes/schema.py
# from fastapi_core.schemas import NoteCreate, NoteResponse, NoteUpdate
from .schema import NoteCreate, NoteResponse, NoteUpdate


class NoteService:
    def __init__(self, repository: NoteRepository, session: AsyncSession) -> None:
        self.repository = repository
        self.session = session

    # IMPROVE: no await / I/O here, so async is unnecessary
    async def list_notes(
        self,
        q: str | None = None,
    ) -> list[NoteResponse]:
        notes = await self.repository.list_notes(q)

        return [NoteResponse.model_validate(note) for note in notes]

    # IMPROVE: same reason, regular def is enough
    async def get_note(self, note_id: int) -> NoteResponse:
        note = await self.repository.get_note(note_id)

        if note is None:
            raise NoteNotFound(note_id)

        return NoteResponse.model_validate(note)

    async def create_note(self, payload: NoteCreate) -> NoteResponse:
        note = Note(**payload.model_dump())

        try:
            self.repository.add(note)

            await self.session.flush()
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise

        await self.session.refresh(note)

        return NoteResponse.model_validate(note)

    def update_note(
        self,
        note_id: int,
        payload: NoteUpdate,
    ) -> NoteResponse:
        if note_id not in self.notes:
            raise NoteNotFound(note_id)

        update_data = payload.model_dump(exclude_unset=True)
        self.notes[note_id].update(update_data)

        current_version = self.notes[note_id]["internal_version"]

        if not isinstance(current_version, int):
            raise RuntimeError("Invalid internal version")

        self.notes[note_id]["internal_version"] = current_version + 1

        return NoteResponse.model_validate(self.notes[note_id])

    def delete_note(self, note_id: int) -> None:
        if note_id not in self.notes:
            raise NoteNotFound(note_id)
        del self.notes[note_id]
