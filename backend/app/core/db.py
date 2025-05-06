from sqlmodel import SQLModel, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)  # echo=True for debugging


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
