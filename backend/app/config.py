from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Anthropic
    anthropic_api_key: str = ""

    # GitHub
    github_token: str = ""
    github_app_id: Optional[str] = None
    github_private_key_path: Optional[str] = None
    github_webhook_secret: str = ""

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./codeguard.db"

    # Analysis settings
    max_diff_lines: int = 1000
    max_inline_comments: int = 10
    analysis_timeout: int = 60  # seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
