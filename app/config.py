import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file() -> str:
    env = os.getenv("ENV", "dev")

    return {
        "prod": ".env.prod",
        "demo": ".env.demo",
        "dev": ".env",
    }.get(env, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = "dev"
    debug: bool = False
    log_level: str = "info"
    database_url: str

    @property
    def db_url(self) -> str:
        return self.database_url

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()