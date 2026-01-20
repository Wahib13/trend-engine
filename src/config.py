import logging
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file="../.env")

    CORS_ALLOWED_ORIGINS: List[str] = []
    DATABASE_CONNECTION_STRING: str = ""
    OLLAMA_MODEL: str = "llama3.1:8b"


settings = Settings()


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
