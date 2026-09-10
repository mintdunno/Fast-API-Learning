import pytest
from fastapi.testclient import TestClient

from fastapi_core.features.notes import router as notes_router
from fastapi_core.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_notes() -> None:
    notes_router.notes.clear()
    notes_router.next_id = 1


def test_create_note() -> None:
    response = client.post(
        "/notes",
        json={
            "title": "Learn FastAPI",
            "content": "Learn API testing",
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "content": "Learn API testing",
    }


def test_create_then_get_note() -> None:
    create_response = client.post(
        "/notes",
        json={
            "title": "FastAPI",
            "content": "HTTP testing",
        },
    )

    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    get_response = client.get(f"/notes/{note_id}")

    assert get_response.status_code == 200

    assert get_response.json() == {
        "id": 1,
        "title": "FastAPI",
        "content": "HTTP testing",
    }


def test_get_missing_note_returns_404() -> None:
    response = client.get("/notes/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Note not found",
    }


def test_create_note_rejects_empty_title() -> None:
    response = client.post(
        "/notes",
        json={
            "title": "",
            "content": "Invalid note",
        },
    )

    assert response.status_code == 422


def test_response_does_not_leak_internal_version() -> None:
    response = client.post(
        "/notes",
        json={
            "title": "FastAPI",
            "content": "Response models",
        },
    )

    assert response.status_code == 201

    assert "internal_version" not in response.json()


def test_patch_updates_only_sent_fields() -> None:
    create_response = client.post(
        "/notes",
        json={
            "title": "Old title",
            "content": "Keep this content",
        },
    )

    note_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "New title",
        },
    )

    assert patch_response.status_code == 200

    assert patch_response.json() == {
        "id": note_id,
        "title": "New title",
        "content": "Keep this content",
    }


def test_patch_rejects_null_title() -> None:
    create_response = client.post(
        "/notes",
        json={
            "title": "FastAPI",
            "content": "HTTP",
        },
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": None,
        },
    )

    assert response.status_code == 422


def test_delete_note_returns_204() -> None:
    create_response = client.post(
        "/notes",
        json={
            "title": "Delete me",
            "content": "Temporary note",
        },
    )

    note_id = create_response.json()["id"]

    response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_list_notes_filters_by_title() -> None:
    client.post(
        "/notes",
        json={
            "title": "Learn FastAPI",
            "content": "Backend",
        },
    )

    client.post(
        "/notes",
        json={
            "title": "Learn PostgreSQL",
            "content": "Database",
        },
    )

    response = client.get(
        "/notes",
        params={
            "q": "fastapi",
        },
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "title": "Learn FastAPI",
            "content": "Backend",
        }
    ]
