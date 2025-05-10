from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from app.core.security import get_password_hash, verify_password
from app.models import UserCreate, User
from app.api.deps import SessionDep


class _UserService:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_user(self, user: UserCreate):
        db_user = User.model_validate(
            user, update={"hashed_password": get_password_hash(user.password)}
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        db_user = self.session.exec(statement).first()
        return db_user

    def autentication(self, username: str, password: str):
        db_user = self.get_user_by_username(username)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user


UserService = Annotated[_UserService, Depends()]
