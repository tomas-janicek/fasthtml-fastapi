from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    BASE_DIR: Path = Path(__file__).parent.parent
    BASE_BE_URL: str = "http://localhost:8000/api/v1/"

    DEFAULT_TIMEOUT: int = 10
    LOGGING_LEVEL: str = "INFO"


settings = Settings()


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
            "filename": "logs/frontend.log",
        },
    },
    "loggers": {
        "root": {
            "level": settings.LOGGING_LEVEL,
            "handlers": ["console", "file"],
        },
    },
}
