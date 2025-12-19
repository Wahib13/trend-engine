from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.initialise import initialise_database
from db.models import Article as ArticleModel, Feed, FeedType, SourceName, Source, Topic


@pytest.fixture
def default_data():
    source_bbc = Source(name=SourceName.BBC)
    source_bbc.feeds = [
        Feed(url="https://feed.test", feed_type=FeedType.POLITICS),
    ]
    default_topics = [
        Topic(name=FeedType.POLITICS.value),
        Topic(name=FeedType.TECHNOLOGY.value),
        Topic(name=FeedType.BUSINESS.value),
        Topic(name=FeedType.HEALTH.value),
    ]
    return [source_bbc, *default_topics]

@pytest.fixture
def db_session(default_data):
    engine = create_engine("sqlite:///:memory:", echo=False)
    connection = engine.connect()
    transaction = connection.begin()

    session_maker_instance = sessionmaker(bind=connection)
    session: Session = session_maker_instance()

    initialise_database(engine, session, default_data)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


class FakeFeedData:
    def __init__(self, entries):
        self.entries = entries


@pytest.fixture
def sample_db_articles():
    return [
        ArticleModel(
            id=1,
            hacker_news_id=1,
            title="AI Lives Rent Free In My Head",
        ),
        ArticleModel(
            id=2,
            hacker_news_id=2,
            title="Python is cool, but my favorite language is Sarcasm",
        ),
    ]


@pytest.fixture
def populated_db_session(
        db_session,
        sample_db_articles,
):
    db_session.add_all(sample_db_articles)
    db_session.commit()
    return db_session
