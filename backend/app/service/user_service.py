from typing import Annotated
from fastapi import Depends, HTTPException
from app.core.security import get_password_hash, verify_password
from app.models import UserCreate, User
from app.api.deps import CurrentUser
from app.models.user import UpdatePassword, UserUpdate
from app.repository.user_repository import UserRepository


class _UserService:
    def __init__(self, user: CurrentUser, user_repo: UserRepository):
        self.user = user
        self.user_repo = user_repo

    def create_user(self, user: UserCreate):
        db_user = User.model_validate(
            user, update={"hashed_password": get_password_hash(user.password)}
        )
        if self.get_user_by_username(db_user.username):
            raise HTTPException(
                status_code=409, detail="This username is already in use"
            )

        if self.get_user_by_email(db_user.email):
            raise HTTPException(status_code=409, detail="This email is already in use")

        self.user_repo.create(db_user)
        return db_user

    def get_user_by_username(self, username: str) -> User | None:
        db_user = self.user_repo.get_by_username(username)
        return db_user

    def get_user_by_email(self, email: str) -> User | None:
        db_user = self.user_repo.get_by_email(email)
        return db_user

    def update_password(self, passwords: UpdatePassword):
        if not verify_password(passwords.current_password, self.user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        if passwords.current_password == passwords.new_password:
            raise HTTPException(
                status_code=400,
                detail="New password must be different from the current one.",
            )
        self.user.hashed_password = get_password_hash(passwords.new_password)
        self.user_repo.update(self.user)
        return self.user

    def update_user(self, user_update: UserUpdate):
        if user_update.username and user_update.username != self.user.username:
            existing_user = self.get_user_by_username(user_update.username)
            if existing_user:
                raise HTTPException(
                    status_code=409, detail="This username is already in use"
                )

        if user_update.email and user_update.email != self.user.email:
            existing_user = self.get_user_by_email(user_update.email)
            if existing_user:
                raise HTTPException(
                    status_code=409, detail="This email is already registered"
                )

        self.user.sqlmodel_update(user_update.model_dump(exclude_unset=True))
        self.user_repo.update(self.user)
        return self.user


UserService = Annotated[_UserService, Depends()]
