from typing import TypeVar, Generic

from app.api.deps import SessionDep

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, entity: T):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T):
        self.session.delete(entity)
        self.session.commit()
