from pydantic import BaseModel, Field, field_validator


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
