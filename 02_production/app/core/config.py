"""Настройки приложения из переменных окружения и файла .env."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Единая типизированная конфигурация приложения."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tic-Tac-Toe API"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tic_tac_toe"
    jwt_secret: str = Field(min_length=32)
    access_token_expire_minutes: int = Field(default=30, gt=0)


@lru_cache
def get_settings() -> Settings:
    """Создать настройки один раз и затем возвращать тот же объект."""

    return Settings()  # type: ignore[call-arg]
