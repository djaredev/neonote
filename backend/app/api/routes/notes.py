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
async def update_note(note: NoteUpdate, service: NoteService, id: UUID):
    updated_note = service.update_note(id, note)
    if not updated_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return updated_note

