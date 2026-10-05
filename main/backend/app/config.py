"""Application settings."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "StudyPlanOptimisation"
    app_env: str = "development"
    debug: bool = True
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'curriculum.db').as_posix()}"
    secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 480
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    uploads_dir: str = str(BASE_DIR / "uploads")
    logs_dir: str = str(BASE_DIR / "logs")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
