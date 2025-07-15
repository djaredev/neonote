from pydantic import DirectoryPath, computed_field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API: str = "/api"
    DB_DIALECT: str = "sqlite"
    DB_DRIVER: str = ""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    DATA_DIR: DirectoryPath
    FRONTEND_DIR: DirectoryPath

    @field_validator("DATA_DIR", "FRONTEND_DIR", mode="after")
    @classmethod
    def resolve_path(cls, value: DirectoryPath) -> DirectoryPath:
        return value.resolve()

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DIALECT}{self.DB_DRIVER}:////{self.DATA_DIR}/neonote.db"

    @computed_field
    @property
    def LOG_PATH(self) -> str:
        return f"{self.DATA_DIR}/logs/app.log"


settings = Settings()  # type: ignore
