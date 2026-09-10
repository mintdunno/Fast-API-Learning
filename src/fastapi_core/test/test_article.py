import pytest
from fastapi.testclient import TestClient

from fastapi_core.main import app
from fastapi_core.features.articles import articles as articles_router

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_articles() -> None:
    articles_router.articles.clear()
    articles_router.next_id = 1


def test_create_article() -> None:
    response = client.post(
        "/articles",
        json={
            "title": "Learn FastAPI",
            "body": "Learn API testing",
            "published": True,
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "body": "Learn API testing",
        "published": True,
    }


def test_create_article_defaults_published_to_false() -> None:
    response = client.post(
        "/articles",
        json={
            "title": "Draft article",
            "body": "Not published yet",
        },
    )

    assert response.status_code == 201

    assert response.json()["published"] is False


def test_create_then_get_article() -> None:
    create_response = client.post(
        "/articles",
        json={
            "title": "FastAPI",
            "body": "HTTP testing",
        },
    )

    assert create_response.status_code == 201

    article_id = create_response.json()["id"]

    get_response = client.get(f"/articles/{article_id}")

    assert get_response.status_code == 200

    assert get_response.json() == {
        "id": 1,
        "title": "FastAPI",
        "body": "HTTP testing",
        "published": False,
    }


def test_get_missing_article_returns_404() -> None:
    response = client.get("/articles/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Article not found",
    }


def test_create_article_rejects_empty_title() -> None:
    response = client.post(
        "/articles",
        json={
            "title": "",
            "body": "Invalid article",
        },
    )

    assert response.status_code == 422


def test_response_does_not_leak_internal_version() -> None:
    response = client.post(
        "/articles",
        json={
            "title": "FastAPI",
            "body": "Response models",
        },
    )

    assert response.status_code == 201

    assert "internal_version" not in response.json()


def test_patch_updates_only_sent_fields() -> None:
    create_response = client.post(
        "/articles",
        json={
            "title": "Old title",
            "body": "Keep this body",
            "published": True,
        },
    )

    article_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/articles/{article_id}",
        json={
            "title": "New title",
        },
    )

    assert patch_response.status_code == 200

    assert patch_response.json() == {
        "id": article_id,
        "title": "New title",
        "body": "Keep this body",
        "published": True,
    }


def test_patch_rejects_null_title() -> None:
    create_response = client.post(
        "/articles",
        json={
            "title": "FastAPI",
            "body": "HTTP",
        },
    )

    article_id = create_response.json()["id"]

    response = client.patch(
        f"/articles/{article_id}",
        json={
            "title": None,
        },
    )

    assert response.status_code == 422


def test_delete_article_returns_204() -> None:
    create_response = client.post(
        "/articles",
        json={
            "title": "Delete me",
            "body": "Temporary article",
        },
    )

    article_id = create_response.json()["id"]

    response = client.delete(f"/articles/{article_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_article_returns_404() -> None:
    response = client.delete("/articles/999")

    assert response.status_code == 404


def test_list_articles_filters_by_title() -> None:
    client.post(
        "/articles",
        json={
            "title": "Learn FastAPI",
            "body": "Backend",
        },
    )

    client.post(
        "/articles",
        json={
            "title": "Learn PostgreSQL",
            "body": "Database",
        },
    )

    response = client.get(
        "/articles",
        params={
            "title": "fastapi",
        },
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "title": "Learn FastAPI",
            "body": "Backend",
            "published": False,
        }
    ]


def test_list_articles_filters_by_published() -> None:
    client.post(
        "/articles",
        json={
            "title": "Published article",
            "body": "Live",
            "published": True,
        },
    )

    client.post(
        "/articles",
        json={
            "title": "Draft article",
            "body": "Hidden",
        },
    )

    response = client.get(
        "/articles",
        params={
            "published": True,
        },
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "title": "Published article",
            "body": "Live",
            "published": True,
        }
    ]
