class ArticleNotFound(Exception):
    def __init__(self, article_id: int) -> None:
        self.article_id = article_id
        super().__init__("Article not found")
