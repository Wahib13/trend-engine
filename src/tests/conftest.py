import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from api.main import app
from db.connection import get_session_dependency
from db.initialise import initialise_database
from db.models import Article as ArticleModel, Feed, FeedType, SourceName, Source, Topic


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
    return [
        ArticleModel(
            title="AI Lives Rent Free In My Head",
            url="https://example.com/article1",
            topics=[fake_topics[0]],
            source=fake_source
        ),
        ArticleModel(
            title="Python is cool, but my favorite language is Sarcasm",
            url="https://example.com/article2",
            topics=[fake_topics[1]],
            source=fake_source
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


@pytest.fixture
def test_client(override_get_session):
    app.dependency_overrides[get_session_dependency] = override_get_session
    return TestClient(app)
