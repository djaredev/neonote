# from sqlmodel import Session
# from app.models import NoteCreate


# def create_note(note: NoteCreate, session: Session):
#     return

from datetime import datetime
from typing import Annotated

from fastapi import Depends
from app.api.deps import SessionDep
from app.models.note import Note, NoteCreate
from app.models.user import User


class _NoteService:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_note(self, user: User, note: NoteCreate):
        db_note = Note.model_validate(
            note,
            update={
                "user_id": user.id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        )
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return db_note


NoteService = Annotated[_NoteService, Depends()]
