# from sqlmodel import Session
# from app.models import NoteCreate


# def create_note(note: NoteCreate, session: Session):
#     return

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from app.api.deps import CurrentUser
from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.utils import Direction
from app.repository.note_repository import NoteRepository


class _NoteService:
    def __init__(self, user: CurrentUser, note_repo: NoteRepository):
        self.user = user
        self.note_repo = note_repo

    def create_note(self, note: NoteCreate):
        db_note = Note.model_validate(
            note,
            update={
                "user_id": self.user.id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        )
        return self.note_repo.create(db_note)

    def get_note(self, id: UUID):
        db_note = self.note_repo.get_by_user(self.user, id)
        if not db_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )
        return db_note

    def get_notes(self, encoded_cursor: str | None, limit: int, direction: Direction):
        return self.note_repo.get_all(self.user, encoded_cursor, limit, direction)

    def get_archived_notes(
        self, encoded_cursor: str | None, limit: int, direction: Direction
    ):
        return self.note_repo.get_all(
            self.user, encoded_cursor, limit, direction, is_archived=True
        )

    def get_trashed_notes(
        self, encoded_cursor: str | None, limit: int, direction: Direction
    ):
        return self.note_repo.get_all(
            self.user, encoded_cursor, limit, direction, is_trashed=True
        )

    def update_note(self, id, note: NoteUpdate):
        db_note = self.get_note(id)
        note_model = note.model_dump(exclude_unset=True)
        note_model["updated_at"] = datetime.now()
        db_note.sqlmodel_update(note_model)
        return self.note_repo.update(db_note)

    def delete_note(self, id):
        db_note = self.get_note(id)
        self.note_repo.delete(db_note)
        return db_note

    def archive_note(self, id: UUID):
        db_note = self.get_note(id)
        db_note.is_archived = True
        self.note_repo.update(db_note)

    def unarchive_note(self, id: UUID):
        db_note = self.get_note(id)
        db_note.is_archived = False
        self.note_repo.update(db_note)

    def trash_note(self, id: UUID):
        db_note = self.get_note(id)
        db_note.is_trashed = True
        self.note_repo.update(db_note)

    def restore_note(self, id: UUID):
        db_note = self.get_note(id)
        db_note.is_trashed = False
        self.note_repo.update(db_note)


NoteService = Annotated[_NoteService, Depends()]
