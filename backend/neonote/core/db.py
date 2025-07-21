from sqlmodel import SQLModel, Session, create_engine, select
from neonote.core.config import settings
from neonote.models import User
from neonote.core.security import get_password_hash
from neonote.core.logger.logger import logger

engine = create_engine(settings.DATABASE_URL)  # echo=True for debugging


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_superuser(session: Session):
    superuser = User(
        username=settings.SUPERUSER_USERNAME,
        email=settings.SUPERUSER_EMAIL,
        hashed_password=get_password_hash(
            settings.SUPERUSER_PASSWORD.get_secret_value()
        ),
        is_superuser=True,
    )
    session.add(superuser)
    session.commit()
    session.refresh(superuser)
    return superuser


def init_db():
    logger.info("Initializing database...")
    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).limit(1)).first()
        if not user:
            logger.info("Creating superuser...")
            create_superuser(session)
            logger.info("Superuser created.")
        else:
            logger.info("Superuser already exists.")
    logger.info("Database initialized.")
