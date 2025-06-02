# from sqlmodel import Session
# from app.models import NoteCreate


# def create_note(note: NoteCreate, session: Session):
#     return

from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlmodel import select
from app.api.deps import CurrentUser, SessionDep
from app.models.note import Note, NoteCreate, NoteUpdate


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

    def get_notes(self):
        return self.session.exec(
            select(Note)
            .where(Note.user_id == self.user.id)
            .where(Note.is_archived == False)
            .where(Note.is_trashed == False)
            .order_by(Note.created_at.desc())  # type: ignore
        )

    def get_archived_notes(self):
        return self.session.exec(
            select(Note)
            .where(Note.user_id == self.user.id)
            .where(Note.is_archived == True)
            .where(Note.is_trashed == False)
            .order_by(Note.created_at.desc())  # type: ignore
        )
    def update_note(self, id, note: NoteUpdate):
        db_note = self.session.get(Note, id)
        if not db_note:
            return None
        if db_note.user_id != self.user.id:
            return None
        note_model = note.model_dump(exclude_unset=True)
        note_model["updated_at"] = datetime.now()
        db_note.sqlmodel_update(note_model)
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return db_note

    def delete_note(self, id):
        db_note = self.session.get(Note, id)
        if not db_note:
            return None
        if db_note.user_id != self.user.id:
            return None
        self.session.delete(db_note)
        self.session.commit()
        return db_note


NoteService = Annotated[_NoteService, Depends()]
