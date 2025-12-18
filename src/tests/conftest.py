from unittest.mock import Mock

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from common.hackernews import HackerNewsItem, Type
from common.topic import Topic
from db.initialise import initialise_database
from db.models import Article as ArticleModel


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    connection = engine.connect()
    transaction = connection.begin()

    session_maker_instance = sessionmaker(bind=connection)
    session: Session = session_maker_instance()

    initialise_database(engine, session)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_hackernews_api():
    api = Mock()
    return api


class FakeTopicModel:
    fake_topics = [
        Topic(id=1, name="AI", representation=[], representative_docs=[]),
        Topic(id=2, name="Python", representation=[], representative_docs=[]),
        Topic(id=3, name="Other", representation=[], representative_docs=[]),
    ]
    def fit(self, documents):
        # no-op
        return self

    def transform(self, title):
        if "AI" in title:
            return (1,), (0.9,)
        if "Python" in title:
            return (2,), (0.9,)
            return "programming"
        return (3,), (0.9,)

    def get_topic_info(self, topic_id):
        return pd.DataFrame({
            "Topic": [self.fake_topics[topic_id - 1].id],
            "Name": [self.fake_topics[topic_id - 1].name],
            "Representation": [self.fake_topics[topic_id - 1].representation],
            "Representative_Docs": [self.fake_topics[topic_id - 1].representative_docs],
        })


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


@pytest.fixture
def sample_hacker_news_items():
    return [
        HackerNewsItem(
            id=1,
            type=Type.STORY,
            text="Hello World",
            url="https://example.com/"
        ),
        HackerNewsItem(
            id=2,
            type=Type.STORY,
            text="Hello World",
            url="https://example.com/"
        )
    ]


@pytest.fixture
def sample_hacker_news_items_with_updates(sample_hacker_news_items):
    updated_stories = sample_hacker_news_items.copy()
    updated_stories[0].text += "updated title"
    return updated_stories


@pytest.fixture
def sample_hacker_news_items_with_new_story(sample_hacker_news_items):
    updated_stories = sample_hacker_news_items.copy()
    updated_stories.append(
        HackerNewsItem(
            id=3,
            type=Type.STORY,
            text="Hello World",
            url="https://example.com/"
        )
    )
    return updated_stories
