from db.models import Article
from ingestion.hackernews import fetch_articles


def test_new_articles(
        mock_hackernews_api,
        db_session,
        sample_articles,
):
    mock_hackernews_api.fetch_articles.return_value = [story.id for story in sample_articles]

    def fetch_story_side_effect(story_id):
        return next(filter(lambda s: s.id == story_id, sample_articles))

    mock_hackernews_api.fetch_story.side_effect = fetch_story_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    db_results = db_session.query(Article).all()

    assert len(db_results) == len(sample_articles)
    for db_story in db_results:
        expected_story = next(filter(lambda story: story.id == db_story.hacker_news_id, sample_articles))
        assert db_story.title == expected_story.title
        assert db_story.url == str(expected_story.url)
        assert db_story.type == expected_story.type.value


def test_update_stories(
        mock_hackernews_api,
        db_session,
        sample_articles,
        sample_stories_with_updates,
):
    """
    an existing story with an updated title should update in the database
    """
    mock_hackernews_api.fetch_articles.return_value = [story.id for story in sample_articles]

    def fetch_story_side_effect(story_id):
        return next(filter(lambda s: s.id == story_id, sample_articles))

    mock_hackernews_api.fetch_story.side_effect = fetch_story_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    # verify initial insert
    db_results = db_session.query(Article).all()
    assert len(db_results) == len(sample_articles)

    mock_hackernews_api.fetch_articles.return_value = [story.id for story in sample_stories_with_updates]

    # update side effect to handle the duplicates
    def fetch_story_with_duplicates_side_effect(story_id):
        return next(s for s in sample_stories_with_updates if s.id == story_id)

    mock_hackernews_api.fetch_story.side_effect = fetch_story_with_duplicates_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    db_results_after = db_session.query(Article).all()

    # length should not increase. upsert should prevent duplicates
    assert len(db_results_after) == len(sample_articles)

    # verify all data is still correct
    for db_story in db_results_after:
        expected_story = next(filter(lambda story: story.id == db_story.hacker_news_id, sample_stories_with_updates))
        assert db_story.title == expected_story.title
        assert db_story.url == str(expected_story.url)
        assert db_story.type == expected_story.type.value


def test_new_story_added(
        mock_hackernews_api,
        db_session,
        sample_articles,
        sample_stories_with_new_story,
):
    """
    after a new story is included in the API it should be stored successfully
    """
    mock_hackernews_api.fetch_articles.return_value = [story.id for story in sample_articles]

    def fetch_story_side_effect(story_id):
        return next(filter(lambda s: s.id == story_id, sample_articles))

    mock_hackernews_api.fetch_story.side_effect = fetch_story_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    # verify initial insert
    db_results = db_session.query(Article).all()
    assert len(db_results) == len(sample_articles)

    mock_hackernews_api.fetch_articles.return_value = [story.id for story in sample_stories_with_new_story]

    # update side effect to handle the duplicates
    def fetch_story_with_duplicates_side_effect(story_id):
        return next(filter(lambda s: s.id == story_id, sample_stories_with_new_story))

    mock_hackernews_api.fetch_story.side_effect = fetch_story_with_duplicates_side_effect

    fetch_articles(
        mock_hackernews_api,
        db_session,
    )

    db_results_after = db_session.query(Article).all()

    # length should increase
    assert len(db_results_after) == len(sample_stories_with_new_story)

    # verify all data is still correct
    for db_story in db_results_after:
        expected_story = next(filter(lambda story: story.id == db_story.hacker_news_id, sample_stories_with_new_story))
        assert db_story.title == expected_story.title
        assert db_story.url == str(expected_story.url)
        assert db_story.type == expected_story.type.value
