from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class Direction(str, Enum):
    NEXT = "next"
    PREV = "prev"


class Cursor(BaseModel):
    id: UUID
    created_at: datetime
