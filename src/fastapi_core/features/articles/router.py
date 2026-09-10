from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from .exception import ArticleNotFound
from .schema import *
from .service import *

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


def get_article_service(request: Request) -> ArticleService:
    return request.app.state.article_service


ArticleServiceDep = Annotated[ArticleService, Depends(get_article_service)]


@router.get("", response_model=list[ArticleResponse])
async def list_articles(
    service: ArticleServiceDep, title: str | None = None, published: bool | None = None
) -> list[ArticleResponse]:
    try:
        return service.list_articles(title, published)
    except ArticleNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, service: ArticleServiceDep) -> ArticleResponse:
    try:
        return service.get_article(article_id)
    except ArticleNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    payload: ArticleCreate, service: ArticleServiceDep
) -> ArticleResponse:
    try:
        return service.create_article(payload)
    except ArticleNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.patch("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int, payload: ArticleUpdate, service: ArticleServiceDep
) -> ArticleResponse:
    try:
        return service.update_article(article_id, payload)
    except ArticleNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def del_article(article_id: int, service: ArticleServiceDep) -> None:
    try:
        return service.del_article(article_id)
    except ArticleNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
