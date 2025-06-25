from uuid import UUID
from fastapi import APIRouter, status

from app.models import NoteCreate
from app.models.note import NotePublic, NoteUpdate, NotesPublic
from app.models.utils import Direction
from app.service.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NotePublic)
async def create_note(note: NoteCreate, service: NoteService):
    new_note = service.create_note(note)
    return new_note


@router.get("", response_model=NotesPublic)
async def get_notes(
    service: NoteService,
    cursor: str | None = None,
    limit: int = 10,
    direction: Direction = Direction.NEXT,
):
    notes, next_cursor = service.get_notes(cursor, limit, direction)
    return NotesPublic(notes=notes, next_cursor=next_cursor)  # type: ignore


@router.get("/archived", response_model=NotesPublic)
async def get_archived_notes(
    service: NoteService,
    cursor: str | None = None,
    limit: int = 10,
    direction: Direction = Direction.NEXT,
):
    archived_notes, next_cursor = service.get_archived_notes(cursor, limit, direction)
    return NotesPublic(notes=archived_notes, next_cursor=next_cursor)  # type: ignore


@router.get("/trashed", response_model=NotesPublic)
async def get_trashed_notes(
    service: NoteService,
    cursor: str | None = None,
    limit: int = 10,
    direction: Direction = Direction.NEXT,
):
    trashed_notes, next_cursor = service.get_trashed_notes(cursor, limit, direction)
    return NotesPublic(notes=trashed_notes, next_cursor=next_cursor)  # type: ignore


@router.put("/{id}", response_model=NotePublic)
async def update_note(note: NoteUpdate, service: NoteService, id: UUID):
    return service.update_note(id, note)


@router.delete("/{id}", response_model=NotePublic)
async def delete_note(service: NoteService, id: UUID):
    return service.delete_note(id)


@router.post("/{id}/archive", status_code=status.HTTP_204_NO_CONTENT)
async def archive_note(service: NoteService, id: UUID):
    service.archive_note(id)


@router.post("/{id}/unarchive", status_code=status.HTTP_204_NO_CONTENT)
async def unarchive_note(service: NoteService, id: UUID):
    service.unarchive_note(id)


@router.post("/{id}/trash", status_code=status.HTTP_204_NO_CONTENT)
async def trash_note(service: NoteService, id: UUID):
    service.trash_note(id)


@router.post("/{id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_note(service: NoteService, id: UUID):
    service.restore_note(id)
        )
