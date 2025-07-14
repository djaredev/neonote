from sqlmodel import SQLModel, Session, create_engine, select
from app.core.logger import logger
from app.core.config import settings
from app.models import User
from app.core.security import get_password_hash

engine = create_engine(settings.DATABASE_URL)  # echo=True for debugging


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_superuser(session: Session):
    session.add(
        User(
            username=settings.SUPERUSER_USERNAME,
            email=settings.SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
        )
    )
    session.commit()


def init_db():
    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).limit(1)).first()
        if not user:
            logger.info("Creating superuser...")
            create_superuser(session)
            logger.info("Superuser created.")
