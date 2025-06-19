from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, min_length=2, max_length=255)
    email: str = Field(unique=True, min_length=2, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(SQLModel):
    username: str | None = Field(default=None, min_length=2, max_length=255)
    email: str | None = Field(default=None, min_length=2, max_length=255)


class UserDelete(SQLModel):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    pass
