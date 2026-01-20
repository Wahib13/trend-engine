from typing import List, Dict
import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from adapters.interfaces import LLMClient
from api.main import app
from db.connection import get_session_dependency
from db.initialise import initialise_database
from db.models import Article as ArticleDB, Feed, FeedType, SourceName, Source, Topic


@pytest.fixture
def fake_source():
    source_bbc = Source(name=SourceName.BBC)
    source_bbc.feeds = [
        Feed(url="https://feed.test", feed_type=FeedType.POLITICS),
    ]
    return source_bbc


@pytest.fixture
def fake_topics():
    return [
        Topic(name=FeedType.TECHNOLOGY.value),
        Topic(name=FeedType.POLITICS.value),
        Topic(name=FeedType.BUSINESS.value),
        Topic(name=FeedType.HEALTH.value),
    ]


@pytest.fixture
def fake_articles(fake_topics, fake_source):
    """Articles with default timestamps (now)"""
    return [
        ArticleDB(
            title="AI Lives Rent Free In My Head",
            url="https://example.com/article1",
            topics=[fake_topics[0]],
            source=fake_source,
            source_topic=FeedType.TECHNOLOGY.value
        ),
        ArticleDB(
            title="Python is cool, but my favorite language is Sarcasm",
            url="https://example.com/article2",
            topics=[fake_topics[1]],
            source=fake_source,
            source_topic=FeedType.POLITICS.value
        ),
    ]


@pytest.fixture
def fake_articles_with_dates(fake_topics, fake_source):
    """Articles with specific creation dates for testing date filtering"""
    now = datetime.datetime.now()
    today = now.date()
    yesterday = today - datetime.timedelta(days=1)
    two_days_ago = today - datetime.timedelta(days=2)
    week_ago = today - datetime.timedelta(days=7)

    return [
        # Articles from today (within past 24 hours) - use explicit times on today's date
        ArticleDB(
            title="Breaking News Today Morning",
            url="https://example.com/today1",
            topics=[fake_topics[0]],
            source=fake_source,
            source_topic=FeedType.TECHNOLOGY.value,
            created=datetime.datetime.combine(today, datetime.time(10, 0, 0))
        ),
        ArticleDB(
            title="Latest Tech Update",
            url="https://example.com/today2",
            topics=[fake_topics[0]],
            source=fake_source,
            source_topic=FeedType.TECHNOLOGY.value,
            created=datetime.datetime.combine(today, datetime.time(18, 30, 0))
        ),
        # Article from yesterday
        ArticleDB(
            title="Yesterday's Big Story",
            url="https://example.com/yesterday",
            topics=[fake_topics[1]],
            source=fake_source,
            source_topic=FeedType.POLITICS.value,
            created=datetime.datetime.combine(yesterday, datetime.time(10, 0, 0))
        ),
        # Article from 2 days ago
        ArticleDB(
            title="Old News from Two Days Ago",
            url="https://example.com/twodays",
            topics=[fake_topics[2]],
            source=fake_source,
            source_topic=FeedType.BUSINESS.value,
            created=datetime.datetime.combine(two_days_ago, datetime.time(15, 30, 0))
        ),
        # Article from a week ago
        ArticleDB(
            title="Ancient Article from Last Week",
            url="https://example.com/week",
            topics=[fake_topics[3]],
            source=fake_source,
            source_topic=FeedType.HEALTH.value,
            created=datetime.datetime.combine(week_ago, datetime.time(9, 0, 0))
        ),
    ]


def make_test_db_session(fake_source, fake_topics, fake_articles):
    engine = create_engine("sqlite:///:memory:", echo=False)
    connection = engine.connect()
    transaction = connection.begin()

    session_maker_instance = sessionmaker(bind=connection)
    session: Session = session_maker_instance()

    initialise_database(engine, session, [*fake_topics, fake_source, *fake_articles])

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def db_session(
        fake_source,
        fake_topics,
        fake_articles,
):
    for session in make_test_db_session(fake_source, fake_topics, fake_articles):
        yield session


@pytest.fixture
def db_session_with_dated_articles(
        fake_source,
        fake_topics,
        fake_articles_with_dates,
):
    """Database session with articles that have specific creation dates"""
    for session in make_test_db_session(fake_source, fake_topics, fake_articles_with_dates):
        yield session


@pytest.fixture
def override_get_session(
        fake_source,
        fake_topics,
        fake_articles
):
    def _override():
        yield from make_test_db_session(fake_source, fake_topics, fake_articles)

    return _override


class FakeFeedData:
    def __init__(self, entries):
        self.entries = entries


class FakeLLM(LLMClient):
    def __init__(self, model: str):
        ...

    def chat(self, messages: List[Dict[str, str]], stream=False, **kwargs) -> str:
        return "Fake response"


@pytest.fixture
def test_client(override_get_session):
    app.dependency_overrides[get_session_dependency] = override_get_session
    return TestClient(app)
