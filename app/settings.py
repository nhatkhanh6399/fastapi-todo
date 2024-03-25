from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core.core_schema import ValidationInfo

PROJECT_DIR = Path(__file__).parent.parent

print(PROJECT_DIR)


class AppSettings(BaseSettings):
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_SERVER: str | None = None
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def build_database_uri(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            print("Loading env file")
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
            port=info.data.get("POSTGRES_PORT"),
        )

    model_config = SettingsConfigDict(env_file=f"{PROJECT_DIR}/.env")


settings = AppSettings()
