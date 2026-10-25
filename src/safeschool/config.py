"""Configuration loaded from environment variables."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SafeSchool PL"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    data_dir: Path = Path("data")
    db_path: Path = Path("data/safeschool.db")
    dane_gov_dataset_id: int = 40
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
