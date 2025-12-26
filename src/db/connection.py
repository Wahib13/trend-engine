from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

import config

engine = create_engine(config.DATABASE_CONNECTION_STRING)
session_maker_instance = sessionmaker(bind=engine)

Base = declarative_base()


@contextmanager
def get_session() -> Generator[Session, Any, None]:
    db = session_maker_instance()
    try:
        yield db
    finally:
        db.close()


def get_session_dependency():
    with get_session() as db:
        yield db
