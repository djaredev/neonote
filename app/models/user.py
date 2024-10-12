from sqlmodel import SQLModel, Field


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
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class ChangePassword(SQLModel):
    old_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
