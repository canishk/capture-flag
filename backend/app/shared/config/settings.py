from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "CipherForge"
    app_env: str = "development"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://cipherforge:cipherforge@localhost:5432/cipherforge"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = Field(
        default="dev-only-change-me-in-production-32chars",
        min_length=32,
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    email_verification_required: bool = False
    password_reset_token_expire_hours: int = 24
    email_verification_token_expire_hours: int = 48

    cors_origins: list[str] = ["http://localhost:3000"]

    storage_path: str = "./storage"
    max_avatar_size_bytes: int = 2_097_152


@lru_cache
def get_settings() -> Settings:
    return Settings()
