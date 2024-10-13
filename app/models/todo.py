from sqlmodel import SQLModel, Field


class TodoBase(SQLModel):
    title: str = Field(max_length=60)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=60)


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    created_at: str
    updated_at: str
    archived: bool = False
    deleted_at: str
    permanently_deleted_at: str


class TaskBase(SQLModel):
    description: str = Field(min_length=1, max_length=255)
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    description: str | None = Field(default=None, min_length=1, max_length=255)
    completed: bool | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    todo_id: int | None = Field(default=None, foreign_key="todo.id")
