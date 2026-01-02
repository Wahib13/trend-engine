import logging
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CORS_ALLOWED_ORIGINS: List[str] = []
    DATABASE_CONNECTION_STRING: str = ""

    class Config:
        env_file = "../.env"


settings = Settings()


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
