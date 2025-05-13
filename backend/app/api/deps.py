from typing import Annotated, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from jwt import InvalidTokenError
from sqlmodel import Session, select
from app.core.db import engine
from app.core.security import decode_token
from app.models.user import User
import uuid

cookie_scheme = APIKeyCookie(name="neonote_token")


def _get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(_get_db)]


def _get_current_user(
    token: Annotated[str, Depends(cookie_scheme)], session: SessionDep
):
    print("Current user: ")
    print("Token: ")
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Try decode...")
        payload = decode_token(token)
        print(payload)
    except InvalidTokenError:
        raise credentials_exception
    user_id: str = payload.get("sub")
    print(user_id)
    if not user_id:
        raise credentials_exception
    user = session.exec(select(User).where(User.id == uuid.UUID(user_id))).first()
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(_get_current_user)]
