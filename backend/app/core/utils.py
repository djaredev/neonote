import base64
import binascii
import json
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.utils import Cursor


def encode_cursor(cursor: Cursor) -> str:
    return base64.urlsafe_b64encode(cursor.model_dump_json().encode()).decode()


def decode_cursor(cursor: str) -> Cursor:
    try:
        return Cursor.model_validate_json(base64.urlsafe_b64decode(cursor).decode())
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError, ValidationError):
        raise HTTPException(status_code=400, detail="Invalid cursor")
