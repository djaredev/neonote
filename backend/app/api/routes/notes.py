from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.models import NoteCreate
from app.service.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("")
async def create_note(user: CurrentUser, note: NoteCreate, service: NoteService):
    new_note = service.create_note(user, note)
    return new_note
