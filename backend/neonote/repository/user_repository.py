from fastapi import Depends
from sqlmodel import select
from neonote.api.deps import SessionDep
from neonote.models.user import User
from neonote.repository.repository import Repository
from typing import Annotated


class _UserRepository(Repository[User]):
    def __init__(self, session: SessionDep):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.exec(select(User).where(User.email == email)).first()

    def get_by_username(self, username: str):
        return self.session.exec(select(User).where(User.username == username)).first()


UserRepository = Annotated[_UserRepository, Depends()]
