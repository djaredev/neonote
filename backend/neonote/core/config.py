from pathlib import Path
from importlib.resources import files
from typing import Annotated
from pydantic import (
    AfterValidator,
    BeforeValidator,
    DirectoryPath,
    FilePath,
    SecretStr,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings
import secrets
import logging

from neonote.core.logger.config_logger import setup_logger


def _mkdir(value: str | DirectoryPath) -> DirectoryPath:
    path = Path(value)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _resolve_path(value: DirectoryPath) -> DirectoryPath:
    return value.resolve()


# Load the required environment variables first to configure logging
class DataDir(BaseSettings):
    DATA_DIR: Annotated[
        DirectoryPath, BeforeValidator(_mkdir), AfterValidator(_resolve_path)
    ] = Path("data/")
    LOG_LEVEL: str = "INFO"

    @computed_field
    @property
    def LOG_PATH(self) -> DirectoryPath:
        return _mkdir(f"{self.DATA_DIR}/logs/") / "neonote.log"


_DataDir = DataDir()  # type: ignore

setup_logger(log_level=_DataDir.LOG_LEVEL, log_path=_DataDir.LOG_PATH)
logger = logging.getLogger("app")


class Settings(DataDir):
    ENVIRONMENT: str = "dev"

    @computed_field
    @property
    def OPENAPI_URL(self) -> str | None:
        if self.ENVIRONMENT != "dev":
            return None
        return f"{self.API}/openapi.json"

    API: str = "/api"
    API_NAME: str = "Neonote API"
    DB_DIALECT: str = "sqlite"
    DB_DRIVER: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: SecretStr
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DIALECT}{self.DB_DRIVER}:////{self.DATA_DIR}/neonote.db"

    SECRET_KEY: SecretStr = SecretStr("")

    @computed_field
    @property
    def SECRET_KEY_FILE(self) -> FilePath:
        secret_key_file = self.DATA_DIR / "secretkey.txt"
        secret_key_file.touch(exist_ok=True)
        return secret_key_file

    @model_validator(mode="after")
    def _create_secret_key(self):
        if self.SECRET_KEY.get_secret_value():
            logger.info("Secret key already exists.")
            return self
        try:
            self.SECRET_KEY = SecretStr(self.SECRET_KEY_FILE.read_text("utf-8"))
            logger.info("Reading secret key from file...")
            if not self.SECRET_KEY.get_secret_value().strip():
                logger.info("Secret key not found, generating new one...")
                self.SECRET_KEY = SecretStr(secrets.token_hex(32))
                self.SECRET_KEY_FILE.write_text(
                    self.SECRET_KEY.get_secret_value(), "utf-8"
                )
                logger.info("New secret key generated and saved to file.")
        except Exception:
            pass
            logger.exception("Error handling secret key from file.")
        return self

    FRONTEND_DIR: Annotated[
        DirectoryPath, BeforeValidator(_mkdir), AfterValidator(_resolve_path)
    ] = files("neonote") / "frontend"  # type: ignore

    @computed_field
    @property
    def FRONTEND_INDEX_PATH(self) -> str:
        return f"{self.FRONTEND_DIR}/index.html"

    @computed_field
    @property
    def FRONTEND_FAVICON_PATH(self) -> str:
        return f"{self.FRONTEND_DIR}/favicon.svg"

    @computed_field
    @property
    def FRONTEND_STATIC_PATH(self) -> DirectoryPath:
        return _mkdir(f"{self.FRONTEND_DIR}/static")


logger.info("Loading configuration...")
# settings = Settings()  # type: ignore

try:
    logger.info("Configuration loaded.")
    settings = Settings()  # type: ignore
except Exception:
    logger.exception("Error loading configuration.")
    raise
