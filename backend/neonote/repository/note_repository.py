from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import and_, col, or_, select
from neonote.api.deps import SessionDep
from neonote.core.utils import decode_cursor, encode_cursor
from neonote.models.note import Note
from neonote.models.user import User
from neonote.models.utils import Cursor, Direction
from neonote.repository.repository import Repository


class _NoteRepository(Repository[Note]):
    def __init__(self, session: SessionDep):
        self.session = session

    def get_by_user(self, user: User, note_id: UUID):
        note = self.session.get(Note, note_id)
        if not note or note.user_id != user.id:
            return None
        return note

    def get_all(
        self,
        user: User,
        encoded_cursor: str | None,
        limit: int,
        direction: Direction,
        is_archived: bool = False,
        is_trashed: bool = False,
    ):
        statement = (
            select(Note)
            .where(Note.user_id == user.id)
            .where(Note.is_archived == is_archived)
            .where(Note.is_trashed == is_trashed)
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


NoteRepository = Annotated[_NoteRepository, Depends()]
