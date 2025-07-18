from typing import Generator
import pytest
from app.models import User, Note
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from app.main import app
from app.core.db import engine
from app.tests.utils.note import create_note_batch
from app.tests.utils.user import (
    create_session_cookie,
    create_test_superuser,
)
from app.service.note_service import _NoteService
from app.repository.note_repository import _NoteRepository


@pytest.fixture(scope="session", autouse=True)
def session() -> Generator[Session, None, None]:
    # create_db_and_tables()
    with Session(engine) as session:
        session.execute(delete(Note))
        session.execute(delete(User))
        session.commit()
        yield session


@pytest.fixture(scope="session")
def init_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def auth_client(session_cookie) -> Generator[TestClient, None, None]:
    with TestClient(app, cookies=session_cookie) as c:
        yield c


@pytest.fixture(scope="session")
def superuser(session: Session):
    yield create_test_superuser(session)
    session.execute(delete(User))
    session.commit()


@pytest.fixture(scope="session")
def session_cookie(superuser: User):
    return create_session_cookie(superuser)


@pytest.fixture()
def note_repo(session: Session):
    return _NoteRepository(session)


@pytest.fixture()
def note_service(superuser: User, note_repo: _NoteRepository):
    return _NoteService(superuser, note_repo)


@pytest.fixture()
def test_notes(note_service: _NoteService, session: Session):
    yield create_note_batch(note_service)
    session.execute(delete(Note))
    session.commit()


@pytest.fixture()
def test_archived_notes(note_service: _NoteService, session: Session):
    yield create_note_batch(note_service, archive=True)
    session.execute(delete(Note))
    session.commit()


@pytest.fixture()
def test_trashed_notes(note_service: _NoteService, session: Session):
    yield create_note_batch(note_service, trash=True)
    session.execute(delete(Note))
    session.commit()
