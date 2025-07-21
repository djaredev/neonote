from typing import Annotated

from fastapi import Depends
from neonote.core.security import verify_password
from neonote.repository.user_repository import UserRepository


class _AuthService:
    def login(self, user_repo: UserRepository, username: str, password: str):
        db_user = user_repo.get_by_username(username)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user


AuthService = Annotated[_AuthService, Depends()]
