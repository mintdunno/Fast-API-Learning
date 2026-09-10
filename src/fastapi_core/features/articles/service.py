from .exception import ArticleNotFound
from .schema import *


class ArticleService:
    def __init__(self) -> None:
        self.articles: dict[int, dict[str, object]] = {}
        self.next_id = 1

    def list_articles(
        self, title: str | None = None, published: bool | None = None
    ) -> list[ArticleResponse]:
        res: list[ArticleResponse] = []
        for article in self.articles.values():
            if title is not None and title.lower() not in str(article["title"]).lower():
                continue
            if published is not None and published != bool(article["published"]):
                continue
            res.append(ArticleResponse.model_validate(article))
        return res

    def get_article(self, article_id: int) -> ArticleResponse:
        if article_id not in self.articles:
            raise ArticleNotFound(article_id)
        return ArticleResponse.model_validate(self.articles[article_id])

    def create_article(self, payload: ArticleCreate) -> ArticleResponse:
        article = {
            "id": self.next_id,
            **payload.model_dump(),
            "internal_version": 1,
        }

        self.articles[self.next_id] = article
        self.next_id += 1

        return ArticleResponse.model_validate(article)

    def update_article(
        self, article_id: int, payload: ArticleCreate
    ) -> ArticleResponse:
        if article_id not in self.articles:
            raise ArticleNotFound(article_id)

        update_data = payload.model_dump(exclude_unset=True)
        self.articles[article_id].update(update_data)

        current_version = self.articles[article_id]["internal_version"]

        if not isinstance(current_version, int):
            raise RuntimeError("Invalid internal version")

        self.articles[article_id]["internal_version"] = current_version + 1

        return ArticleResponse.model_validate(self.articles[article_id])

    def del_article(self, article_id: int) -> None:
        if article_id not in self.articles:
            raise ArticleNotFound(article_id)

        del self.articles[article_id]
