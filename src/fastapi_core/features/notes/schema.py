from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )
    content: str = Field(
        max_length=5000,
    )


class NoteUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    content: str | None = Field(
        default=None,
        max_length=5000,
    )

    @field_validator("title", "content")
    @classmethod
    def reject_null(
        cls,
        value: str | None,
    ) -> str:
        if value is None:
            raise ValueError("Field cannot be null")

        return value


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
