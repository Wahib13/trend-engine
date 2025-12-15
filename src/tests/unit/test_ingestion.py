from db.models import Article
from ingestion.hackernews import fetch_articles


def test_new_articles(
        mock_hackernews_api,
        db_session,
        sample_hacker_news_items,
):
    mock_hackernews_api.fetch_hacker_news_items.return_value = [hacker_news_item.id for hacker_news_item in sample_hacker_news_items]

    def fetch_hacker_news_item_side_effect(hacker_news_item_id):
        return next(filter(lambda s: s.id == hacker_news_item_id, sample_hacker_news_items))

    mock_hackernews_api.fetch_hacker_news_item.side_effect = fetch_hacker_news_item_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    db_results = db_session.query(Article).all()

    assert len(db_results) == len(sample_hacker_news_items)
    for db_article in db_results:
        expected_article = next(filter(lambda article: article.id == db_article.hacker_news_id, sample_hacker_news_items))
        assert db_article.title == expected_article.title
        assert db_article.url == str(expected_article.url)
        assert db_article.type == expected_article.type.value


def test_update_stories(
        mock_hackernews_api,
        db_session,
        sample_hacker_news_items,
        sample_hacker_news_items_with_updates,
):
    """
    an existing article with an updated title should update in the database
    """
    mock_hackernews_api.fetch_hacker_news_items.return_value = [hacker_news_item.id for hacker_news_item in sample_hacker_news_items]

    def fetch_hacker_news_item_side_effect(hacker_news_item_id):
        return next(filter(lambda s: s.id == hacker_news_item_id, sample_hacker_news_items))

    mock_hackernews_api.fetch_hacker_news_item.side_effect = fetch_hacker_news_item_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    # verify initial insert
    db_results = db_session.query(Article).all()
    assert len(db_results) == len(sample_hacker_news_items)

    mock_hackernews_api.fetch_hacker_news_items.return_value = [hacker_news_item.id for hacker_news_item in sample_hacker_news_items_with_updates]

    # update side effect to handle the duplicates
    def fetch_hacker_news_item_side_effect(hacker_news_item_id):
        return next(s for s in sample_hacker_news_items_with_updates if s.id == hacker_news_item_id)

    mock_hackernews_api.fetch_hacker_news_item.side_effect = fetch_hacker_news_item_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    db_results_after = db_session.query(Article).all()

    # length should not increase. upsert should prevent duplicates
    assert len(db_results_after) == len(sample_hacker_news_items)

    # verify all data is still correct
    for db_article in db_results_after:
        expected_article = next(filter(lambda hacker_news_item: hacker_news_item.id == db_article.hacker_news_id, sample_hacker_news_items_with_updates))
        assert db_article.title == expected_article.title
        assert db_article.url == str(expected_article.url)
        assert db_article.type == expected_article.type.value


def test_new_article_added(
        mock_hackernews_api,
        db_session,
        sample_hacker_news_items,
        sample_hacker_news_items_with_new_story,
):
    """
    after a new HackerNewsItem is included in the API it should be stored successfully
    """
    mock_hackernews_api.fetch_hacker_news_items.return_value = [hacker_news_item.id for hacker_news_item in sample_hacker_news_items]

    def fetch_hacker_news_item_side_effect(hacker_news_item_id):
        return next(filter(lambda s: s.id == hacker_news_item_id, sample_hacker_news_items))

    mock_hackernews_api.fetch_hacker_news_item.side_effect = fetch_hacker_news_item_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    # verify initial insert
    db_results = db_session.query(Article).all()
    assert len(db_results) == len(sample_hacker_news_items)

    mock_hackernews_api.fetch_hacker_news_items.return_value = [hacker_news_item.id for hacker_news_item in sample_hacker_news_items_with_new_story]

    # update side effect to handle the duplicates
    def fetch_hacker_news_item_side_effect(hacker_news_item_id):
        return next(filter(lambda s: s.id == hacker_news_item_id, sample_hacker_news_items_with_new_story))

    mock_hackernews_api.fetch_hacker_news_item.side_effect = fetch_hacker_news_item_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    db_results_after = db_session.query(Article).all()

    # length should increase
    assert len(db_results_after) == len(sample_hacker_news_items_with_new_story)

    # verify all data is still correct
    for db_article in db_results_after:
        expected_article = next(filter(lambda hacker_news_item: hacker_news_item.id == db_article.hacker_news_id, sample_hacker_news_items_with_new_story))
        assert db_article.title == expected_article.title
        assert db_article.url == str(expected_article.url)
        assert db_article.type == expected_article.type.value
