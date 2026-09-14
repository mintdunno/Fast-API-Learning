from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Note


class NoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_notes(self, q: str | None = None) -> list[Note]:
        stmt = select(Note).order_by(Note.id)

        if q is not None:
            stmt = stmt.where(Note.title.ilike(f"%{q}%"))

        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_note(self, note_id: int) -> Note | None:
        return await self.session.get(Note, note_id)

    def add(self, note: Note) -> None:
        self.session.add(note)

    async def delete(self, note: Note) -> None:
        await self.session.delete(note)
