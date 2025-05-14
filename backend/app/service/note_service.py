# from sqlmodel import Session
# from app.models import NoteCreate


# def create_note(note: NoteCreate, session: Session):
#     return

from datetime import datetime
from typing import Annotated

from fastapi import Depends
from app.models.note import Note, NoteCreate
from app.models.user import User
from app.api.deps import CurrentUser, SessionDep


class _NoteService:
    def __init__(self, user: CurrentUser, session: SessionDep):
        self.session = session
        self.user = user

    def create_note(self, note: NoteCreate):
        db_note = Note.model_validate(
            note,
            update={
                "user_id": self.user.id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        )
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return db_note


NoteService = Annotated[_NoteService, Depends()]
