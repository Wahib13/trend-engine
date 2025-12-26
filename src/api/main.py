from fastapi import FastAPI, Depends

from api.models import ArticleList, Article, Topic, TopicList
from db.connection import get_session_dependency
from db.models import Article as ArticleDB
from db.models import Topic as TopicDB

app = FastAPI()


@app.get("/articles/")
def get_articles(
        session=Depends(get_session_dependency)
) -> list[ArticleList]:
    articles = session.query(ArticleDB).all()
    return articles


@app.get("/topics/")
def get_topics(
        session=Depends(get_session_dependency)
) -> list[TopicList]:
    topics = session.query(TopicDB).all()
    return topics


@app.get("/topic/{topic_id}/")
def get_topic(
        topic_id: int,
        session=Depends(get_session_dependency)
) -> Topic:
    topic = session.query(TopicDB).filter_by(id=topic_id).first()
    return topic


@app.get("/article/{article_id}/")
def get_article(
        article_id: int,
        session=Depends(get_session_dependency)
) -> Article:
    article = session.query(ArticleDB).filter_by(id=article_id).first()
    return article
