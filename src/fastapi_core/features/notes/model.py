from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_core.db_base import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(5000))
