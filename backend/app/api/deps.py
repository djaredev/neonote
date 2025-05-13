from typing import Annotated, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlmodel import Session, select
from app.core.db import engine
from app.core.security import decode_token
from app.models.user import User
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
cookie_scheme = APIKeyCookie(name="neonote_token")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_current_user(token: str, session: Session):
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


async def get_current_user_token(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)
) -> User:
    return get_current_user(token, session)


async def get_current_user_cookie(
    token: Annotated[str, Depends(cookie_scheme)], session: Session = Depends(get_db)
) -> User:
    return get_current_user(token, session)


SessionDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user_token)]
UserCookie = Annotated[User, Depends(get_current_user_cookie)]
