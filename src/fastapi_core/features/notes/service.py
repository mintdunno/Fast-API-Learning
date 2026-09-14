from sqlalchemy.ext.asyncio import AsyncSession

from .exception import NoteNotFound
from .model import Note
from .repository import NoteRepository
from .schema import NoteCreate, NoteResponse, NoteUpdate


class NoteService:
    def __init__(
        self,
        repository: NoteRepository,
        session: AsyncSession,
    ) -> None:
        self.repository = repository
        self.session = session

    async def list_notes(
        self,
        q: str | None = None,
    ) -> list[NoteResponse]:
        notes = await self.repository.list_notes(q)

        return [NoteResponse.model_validate(note) for note in notes]

    async def get_note(
        self,
        note_id: int,
    ) -> NoteResponse:
        note = await self.repository.get_note(note_id)

        if note is None:
            raise NoteNotFound(note_id)

        return NoteResponse.model_validate(note)

    async def create_note(
        self,
        payload: NoteCreate,
    ) -> NoteResponse:
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

    async def update_note(
        self,
        note_id: int,
        payload: NoteUpdate,
    ) -> NoteResponse:
        note = await self.repository.get_note(note_id)

        if note is None:
            raise NoteNotFound(note_id)

        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(note, field, value)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        await self.session.refresh(note)

        return NoteResponse.model_validate(note)

    async def delete_note(
        self,
        note_id: int,
    ) -> None:
        note = await self.repository.get_note(note_id)

        if note is None:
            raise NoteNotFound(note_id)

        try:
            await self.repository.delete(note)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
