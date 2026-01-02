import logging

import os
from pydantic_settings import BaseSettings
from typing import List


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
