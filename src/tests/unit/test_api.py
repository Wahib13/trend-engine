from db.models import Article


def test_get_topics(
        test_client,
):
    response = test_client.get("/topics/")
    assert response.status_code == 200
    assert len(response.json()) == 4
    # for topic in response.json():
    #     db_topic = list(filter(lambda a: a.id == topic["id"], sample_db_topics))[0]
    #     assert topic["name"] == db_topic.name


def test_get_topic(
        test_client
):
    """
    get the details of a single topic but also doubles as a filter for articles by topic
    """
    test_id = 1
    response = test_client.get(f"/topic/{test_id}/")
    assert response.status_code == 200
    assert response.json()["id"] == test_id


def test_get_articles(
        test_client,
        fake_articles,
):
    response = test_client.get("/articles/")
    assert response.status_code == 200
    assert len(response.json()) == len(fake_articles)
    for article in response.json():
        db_article = list(filter(lambda a: a.id == article["id"], fake_articles))[0]
        assert article["title"] == db_article.title


def test_get_article(
        test_client,
):
    test_id = 1
    response = test_client.get(f"/article/{test_id}/")
    assert response.status_code == 200
    assert response.json()["id"] == test_id
