import secrets
import warnings
from pathlib import Path
from typing import Annotated, Any, Literal, Self

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v  # type: ignore
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DEFAULT_TIMEOUT: int = 10
    BASE_BE_URL: str = "http://localhost:8000/api/v1/"

    BASE_DIR: Path = Path(__file__).parent.parent

    LOGGING_LEVEL: str = "INFO"

    @computed_field
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str

    DB_SCHEMA: str
    DB_SERVER: str | None = None
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        db_url = URL.create(
            drivername=self.DB_SCHEMA,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_SERVER,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )
        return str(db_url)

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)

        return self


settings = Settings()  # type: ignore


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "[%(asctime)s][%(levelname)s]: %(message)s"},
        "rich": {"format": "%(message)s", "datefmt": "[%x %X]"},
    },
    "handlers": {
        "console": {
            "level": settings.LOGGING_LEVEL,
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "markup": True,
            "show_path": True,
        },
        "file": {
            "level": settings.LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "backupCount": 1,
            "filename": "logs/api.log",
        },
        "sqlalchemy_file": {
            "level": settings.LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "backupCount": 1,
            "filename": "logs/sqlalchemy.log",
        },
    },
    "loggers": {
        "root": {
            "level": settings.LOGGING_LEVEL,
            "handlers": ["console", "file"],
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "TRACE",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "TRACE",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "TRACE",
            "propagate": False,
        },
        "uvicorn.asgi": {
            "handlers": ["console", "file"],
            "level": "TRACE",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["sqlalchemy_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
