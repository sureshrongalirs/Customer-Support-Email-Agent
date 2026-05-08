"""Application Configuration and Settings Management"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    env: Literal["development", "production"] = "development"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Customer Support Email Agent API"
    api_version: str = "0.1.0"

    openai_api_key: str
    openai_model: str = "gpt-4"

    log_level: str = "INFO"

    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""

    smtp_server: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    knowledge_base_path: str = "./knowledge_base"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
