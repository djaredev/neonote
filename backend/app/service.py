from sqlmodel import Session, select
from app.core.security import get_password_hash
from app.models.user import UserCreate, User
from app.core.security import verify_password


def create_user(user: UserCreate, session: Session):
    db_user = User.model_validate(
        user, update={"hashed_password": get_password_hash(user.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_username(username: str, session: Session) -> User | None:
    statement = select(User).where(User.username == username)
    db_user = session.exec(statement).first()
    return db_user


def autentication(username: str, password: str, session: Session):
    db_user = get_user_by_username(username, session)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
