from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status

from app.models import NoteCreate
from app.models.note import NotePublic, NoteUpdate, NotesPublic
from app.service.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NotePublic)
async def create_note(note: NoteCreate, service: NoteService):
    new_note = service.create_note(note)
    return new_note
