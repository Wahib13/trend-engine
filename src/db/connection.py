from contextlib import contextmanager
import logging
import time
from typing import Any, Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, declarative_base

import config

logger = logging.getLogger(__name__)

Base = declarative_base()

# The engine and session factory are created lazily on first use rather than at
# import time, so importing this module (for Base, get_session, etc.) does not
# require a DATABASE_CONNECTION_STRING. Tests, alembic and tooling can import it
# with no .env; a genuinely missing/invalid URL then fails loudly at first DB
# use instead of as a cryptic import-time error.
_engine = None
_session_maker = None


def _register_debug_listeners(target_engine) -> None:
    @event.listens_for(target_engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany) -> None:
        conn.info.setdefault("query_start_time", []).append(time.perf_counter())
        logger.warning("SQL query start")

    @event.listens_for(target_engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany) -> None:
        total = time.perf_counter() - conn.info["query_start_time"].pop()
        logger.warning("SQL query end duration=%.3fs", total)


def get_engine():
    global _engine
    if _engine is None:
        url = config.settings.DATABASE_CONNECTION_STRING
        if not url:
            raise RuntimeError(
                "DATABASE_CONNECTION_STRING is not set. "
                "Set it in the environment or .env before using the database."
            )
        _engine = create_engine(url, echo=config.settings.DEBUG)
        if config.settings.DEBUG:
            _register_debug_listeners(_engine)
    return _engine


def get_session_maker():
    global _session_maker
    if _session_maker is None:
        _session_maker = sessionmaker(bind=get_engine())
    return _session_maker


@contextmanager
def get_session() -> Generator[Session, Any, None]:
    db = get_session_maker()()
    try:
        yield db
    finally:
        db.close()


def get_session_dependency():
    with get_session() as db:
        yield db
