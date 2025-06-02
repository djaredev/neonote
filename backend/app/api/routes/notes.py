from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.models import NoteCreate
from app.models.note import NotePublic, NoteUpdate, NotesPublic
from app.service.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NotePublic)
async def create_note(note: NoteCreate, service: NoteService):
    new_note = service.create_note(note)
    return new_note


@router.get("", response_model=NotesPublic)
async def get_notes(service: NoteService):
    notes = service.get_notes()
    return NotesPublic(notes=notes)  # type: ignore


@router.put("/{id}")
@router.get("/archived", response_model=NotesPublic)
async def get_archived_notes(service: NoteService):
    archived_notes = service.get_archived_notes()
    return NotesPublic(notes=archived_notes)  # type: ignore


@router.get("/trashed", response_model=NotesPublic)
async def get_trashed_notes(service: NoteService):
    trashed_notes = service.get_trashed_notes()
    return NotesPublic(notes=trashed_notes)  # type: ignore


@router.put("/{id}", response_model=NotePublic)
async def update_note(note: NoteUpdate, service: NoteService, id: UUID):
    updated_note = service.update_note(id, note)
    if not updated_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return updated_note


@router.delete("/{id}", response_model=NotePublic)
async def delete_note(service: NoteService, id: UUID):
    deleted_note = service.delete_note(id)
    if not deleted_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return deleted_note


@router.post("/{id}/archive", status_code=status.HTTP_204_NO_CONTENT)
async def archive_note(service: NoteService, id: UUID):
    if not service.archive_note(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )


@router.post("/{id}/unarchive", status_code=status.HTTP_204_NO_CONTENT)
async def unarchive_note(service: NoteService, id: UUID):
    if not service.unarchive_note(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )


