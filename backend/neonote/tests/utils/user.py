from sqlmodel import Session

from neonote.core.db import create_superuser
from neonote.core.security import create_access_token
from neonote.models import User


def create_session_cookie(user: User):
    access_token = create_access_token(user.id)
    return {"neonote_token": access_token}


def create_test_superuser(session: Session):
    return create_superuser(session)
