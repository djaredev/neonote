from typing import List
from fastapi import status
from fastapi.testclient import TestClient

from neonote.core.config import settings
from neonote.models.note import Note, NoteCreate, NotePublic, NoteUpdate, NotesPublic
from neonote.models.utils import Direction

PREFIX = f"{settings.API}/notes"


# CRUD operations


def test_create_note(auth_client: TestClient):
    note = NoteCreate(title="test note", content="test note content")
    response = auth_client.post(
        PREFIX,
        json=note.model_dump(),
    )
    assert response.status_code == 200
    NotePublic.model_validate(response.json())
    assert note == NoteCreate.model_validate(response.json())


def test_get_notes(auth_client: TestClient, test_notes):
    response = auth_client.get(
        PREFIX,
        params={"limit": 5, "direction": Direction.NEXT.value},
    )
    assert response.status_code == 200
    data = NotesPublic.model_validate(response.json())
    assert len(data.notes) == 5


def test_update_note(auth_client: TestClient, test_notes: List[Note]):
    update_note = NoteUpdate(title="updated test title", content="updated test content")
    response = auth_client.put(
        f"{PREFIX}/{test_notes[0].id}",
        json=update_note.model_dump(),
    )
    assert response.status_code == 200
    NotePublic.model_validate(response.json())
    assert update_note == NoteUpdate.model_validate(response.json())


def test_delete_note(auth_client: TestClient, test_notes: List[Note]):
    response = auth_client.delete(f"{PREFIX}/{test_notes[0].id}")
    assert response.status_code == status.HTTP_200_OK
    deleted_note = NotePublic.model_validate(response.json())
    assert test_notes[0].id == deleted_note.id


# Without auth


def test_get_notes_without_auth(client: TestClient):
    response = client.get(
        PREFIX,
        params={"limit": 10, "direction": Direction.NEXT.value},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_note_without_auth(client: TestClient):
    note = NoteCreate(title="test note", content="test note content")
    response = client.post(
        PREFIX,
        json=note.model_dump(),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_note_without_auth(client: TestClient, test_notes: List[Note]):
    update_note = NoteUpdate(title="updated test title", content="updated test content")
    response = client.put(
        f"{PREFIX}/{test_notes[0].id}",
        json=update_note.model_dump(),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_note_without_auth(client: TestClient, test_notes: List[Note]):
    response = client.delete(f"{PREFIX}/{test_notes[0].id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# Invalid data


def test_get_notes_with_invalid_cursor(auth_client: TestClient, test_notes: List[Note]):
    response = auth_client.get(
        PREFIX,
        params={
            "cursor": "invalid_data",
            "limit": 10,
            "direction": Direction.NEXT.value,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid cursor"}


def test_get_notes_with_invalid_direction(
    auth_client: TestClient, test_notes: List[Note]
):
    response = auth_client.get(
        PREFIX,
        params={
            "limit": 10,
            "direction": "invalid_direction",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_notes_with_invalid_limit(auth_client: TestClient, test_notes: List[Note]):
    response = auth_client.get(
        PREFIX,
        params={
            "limit": "invalid_limit",
            "direction": Direction.NEXT.value,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ARCHIVE operations


def test_get_archived_notes(auth_client: TestClient, test_archived_notes: List[Note]):
    response = auth_client.get(
        f"{PREFIX}/archived",
        params={"limit": 10, "direction": Direction.NEXT.value},
    )
    assert response.status_code == 200
    data = NotesPublic.model_validate(response.json())
    assert len(data.notes) == 10


def test_archive_note(auth_client: TestClient, test_notes: List[Note]):
    response = auth_client.post(
        f"{PREFIX}/{test_notes[0].id}/archive",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_unarchive_note(auth_client: TestClient, test_archived_notes: List[Note]):
    response = auth_client.post(
        f"{PREFIX}/{test_archived_notes[0].id}/unarchive",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


# WITHOUT AUTH


def test_get_archived_notes_without_auth(client: TestClient):
    response = client.get(
        f"{PREFIX}/archived",
        params={"limit": 10, "direction": Direction.NEXT.value},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_archive_note_without_auth(client: TestClient, test_notes: List[Note]):
    response = client.post(
        f"{PREFIX}/{test_notes[0].id}/archive",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unarchive_note_without_auth(
    client: TestClient, test_archived_notes: List[Note]
):
    response = client.post(
        f"{PREFIX}/{test_archived_notes[0].id}/unarchive",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


# TRASH operations


def test_get_trashed_notes(auth_client: TestClient, test_trashed_notes: List[Note]):
    response = auth_client.get(
        f"{PREFIX}/trashed",
        params={"limit": 10, "direction": Direction.NEXT.value},
    )
    assert response.status_code == 200
    data = NotesPublic.model_validate(response.json())
    assert len(data.notes) == 10


def test_trash_note(auth_client: TestClient, test_notes: List[Note]):
    response = auth_client.post(
        f"{PREFIX}/{test_notes[0].id}/trash",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_restore_note(auth_client: TestClient, test_trashed_notes: List[Note]):
    response = auth_client.post(
        f"{PREFIX}/{test_trashed_notes[0].id}/restore",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


# WITHOUT AUTH


def test_get_trashed_notes_without_auth(client: TestClient):
    response = client.get(
        f"{PREFIX}/trashed",
        params={"limit": 10, "direction": Direction.NEXT.value},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_trash_note_without_auth(client: TestClient, test_notes: List[Note]):
    response = client.post(
        f"{PREFIX}/{test_notes[0].id}/trash",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_restore_note_without_auth(client: TestClient, test_trashed_notes: List[Note]):
    response = client.post(
        f"{PREFIX}/{test_trashed_notes[0].id}/restore",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
