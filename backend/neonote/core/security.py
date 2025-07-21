from datetime import datetime, timedelta, timezone
from typing import Any
from passlib.context import CryptContext
import jwt
from neonote.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str | Any) -> str:
    encode = {
        "sub": str(subject),
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Any:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload


def verify_password(plan_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plan_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
