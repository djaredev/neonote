# from sqlmodel import Session
# from app.models import NoteCreate


# def create_note(note: NoteCreate, session: Session):
#     return

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import col, select, or_, and_
from app.api.deps import CurrentUser, SessionDep
from app.core.utils import decode_cursor, encode_cursor
from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.utils import Cursor, Direction


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

    def get_notes(self, encoded_cursor: str | None, limit: int, direction: Direction):
        statement = (
            select(Note)
            .where(Note.user_id == self.user.id)
            .where(Note.is_archived == False)
            .where(Note.is_trashed == False)
        )
        if encoded_cursor:
            cursor = decode_cursor(encoded_cursor)
            if direction == Direction.NEXT:
                statement = statement.where(
                    or_(
                        Note.created_at < cursor.created_at,
                        and_(Note.created_at == cursor.created_at, Note.id < cursor.id),
                    )
                ).order_by(col(Note.created_at).desc(), col(Note.id).desc())
            else:
                statement = statement.where(
                    or_(
                        Note.created_at > cursor.created_at,
                        and_(Note.created_at == cursor.created_at, Note.id > cursor.id),
                    )
                ).order_by(col(Note.created_at).asc(), col(Note.id).asc())
        else:
            statement = statement.order_by(
                col(Note.created_at).desc(), col(Note.id).desc()
            )
        notes = self.session.exec(statement.limit(limit)).all()
        if not notes:
            return [], None
        return notes, encode_cursor(
            Cursor(id=notes[-1].id, created_at=notes[-1].created_at)
        )

    def get_archived_notes(self):
        return self.session.exec(
            select(Note)
            .where(Note.user_id == self.user.id)
            .where(Note.is_archived == True)
            .where(Note.is_trashed == False)
            .order_by(Note.created_at.desc())  # type: ignore
        )

    def get_trashed_notes(self):
        return self.session.exec(
            select(Note)
            .where(Note.user_id == self.user.id)
            .where(Note.is_trashed == True)
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

    def archive_note(self, id: UUID) -> bool:
        db_note = self.session.get(Note, id)
        if not db_note:
            return False
        if db_note.user_id != self.user.id:
            return False
        db_note.is_archived = True
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return True

    def unarchive_note(self, id: UUID) -> bool:
        db_note = self.session.get(Note, id)
        if not db_note:
            return False
        if db_note.user_id != self.user.id:
            return False
        db_note.is_archived = False
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return True

    def trash_note(self, id: UUID) -> bool:
        db_note = self.session.get(Note, id)
        if not db_note:
            return False
        if db_note.user_id != self.user.id:
            return False
        db_note.is_trashed = True
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return True

    def restore_note(self, id: UUID) -> bool:
        db_note = self.session.get(Note, id)
        if not db_note:
            return False
        if db_note.user_id != self.user.id:
            return False
        db_note.is_trashed = False
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return True


NoteService = Annotated[_NoteService, Depends()]
