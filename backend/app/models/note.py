from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class NoteBase(SQLModel):
    title: str = Field(max_length=60)
    content: str = Field(max_length=10000)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(SQLModel):
    title: str | None = Field(max_length=60)
    content: str | None = Field(max_length=10000)


class Note(NoteBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    deleted_at: datetime | None = None
    is_archived: bool = False
    is_trashed: bool = False
