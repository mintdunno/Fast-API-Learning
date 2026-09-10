from fastapi import APIRouter, HTTPException, status

from fastapi_core.schemas import (
    ArticleCreate,
    ArticleResponse,
    ArticleUpdate,
)

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)

articles: dict[int, dict[str, object]] = {}
next_id = 1


@router.get("", response_model=list[ArticleResponse])
async def list_articles(
    title: str | None = None, published: bool | None = None
) -> list[ArticleResponse]:
    res: list[ArticleResponse] = []
    for article in articles.values():
        if title is not None and title.lower() not in str(article["title"]).lower():
            continue
        if published is not None and published != bool(article["published"]):
            continue
        res.append(ArticleResponse.model_validate(article))

    return res


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int) -> ArticleResponse:
    if article_id not in articles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    return ArticleResponse.model_validate(articles[article_id])


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(payload: ArticleCreate) -> ArticleResponse:
    global next_id

    article: dict[str, object] = {
        "id": next_id,
        **payload.model_dump(),
        "internal_version": 1,
    }
    articles[next_id] = article
    next_id += 1

    return ArticleResponse.model_validate(article)


@router.patch("/{article_id}", response_model=ArticleResponse)
async def update_article(article_id: int, payload: ArticleUpdate) -> ArticleResponse:
    if article_id not in articles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    update_data = payload.model_dump(exclude_unset=True)
    articles[article_id].update(update_data)

    internal_version = articles[article_id]["internal_version"]
    if not isinstance(internal_version, int):
        raise RuntimeError("Invalid internal version")

    articles[article_id]["internal_version"] = internal_version + 1
    return ArticleResponse.model_validate(articles[article_id])


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_article(article_id: int) -> None:
    if article_id not in articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No found")

    del articles[article_id]
