from __future__ import annotations
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://tableorder:tableorder@db:5432/tableorder"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 16
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    upload_dir: str = "/app/uploads"
    log_level: str = "INFO"
    max_login_attempts: int = 5
    lockout_minutes: int = 15

    model_config = {"env_file": ".env"}


settings = Settings()
