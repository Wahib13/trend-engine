from fastapi import FastAPI, Depends, Query
from starlette.middleware.cors import CORSMiddleware

import config
from api.models import ArticleList, Article, Topic, TopicList
from db.connection import get_session_dependency
from db.models import Article as ArticleDB
from db.models import Topic as TopicDB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/articles/")
def get_articles(
        topic_id: int | None = Query(default=None),
        session=Depends(get_session_dependency)
) -> list[ArticleList]:
    query = session.query(ArticleDB)

    if topic_id is not None:
        query = (
            query
            .join(ArticleDB.topics)
            .filter(TopicDB.id == topic_id)
        )

    return query.all()


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
