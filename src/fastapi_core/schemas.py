from pydantic import BaseModel, Field, field_validator


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


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    body: str = Field(min_length=1, max_length=10000)
    published: bool = False


class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    body: str | None = Field(default=None, min_length=1, max_length=10000)
    published: bool = False

    @field_validator("title", "body")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Field cannot be null")
        return value


class ArticleResponse(BaseModel):
    id: int
    title: str
    body: str
    published: bool
