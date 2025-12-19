import feedparser

from db.models import Article, FeedType
from ingestion.main import fetch_rss_entries
from tests.conftest import FakeFeedData


def test_new_articles(db_session, default_data, monkeypatch):
    fake_entries = [
        {"link": "https://example.com/a1", "title": "Article 1"},
        {"link": "https://example.com/a2", "title": "Article 2"},
    ]

    def fake_parse(url):
        return FakeFeedData(fake_entries)

    monkeypatch.setattr(feedparser, "parse", fake_parse)

    # Act
    articles = fetch_rss_entries(db_session)

    # Assert
    assert len(articles) == 2

    urls = {a.url for a in articles}
    assert urls == {
        "https://example.com/a1",
        "https://example.com/a2",
    }

    for article in articles:
        assert article.source == default_data[0]
        assert article.source_topic == FeedType.POLITICS.value


def test_new_articles_skips_duplicates(db_session, default_data, monkeypatch):
    existing = Article(
        url="https://example.com/a1",
        title="Existing",
        source_topic=FeedType.TECHNOLOGY.value,
        source=default_data[0],
    )

    db_session.add(existing)
    db_session.commit()

    fake_entries = [
        {"link": "https://example.com/a1", "title": "Duplicate"},
    ]

    monkeypatch.setattr(
        feedparser,
        "parse",
        lambda _: FakeFeedData(fake_entries),
    )

    articles = fetch_rss_entries(db_session)

    assert articles == []
