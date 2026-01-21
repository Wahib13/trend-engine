import datetime

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import joinedload
from starlette.middleware.cors import CORSMiddleware

import config
from api.models import ArticleList, Article, Topic, TopicList, DailyTrendSummaryList
from db.connection import get_session_dependency
from db.models import Article as ArticleDB
from db.models import Topic as TopicDB
from db.models import DailyTrendSummary as DailyTrendSummaryDB

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
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=50, ge=1, le=100),
        session=Depends(get_session_dependency)
) -> list[ArticleList]:
    query = session.query(ArticleDB)

    if topic_id is not None:
        query = (
            query
            .join(ArticleDB.topics)
            .filter(TopicDB.id == topic_id)
        )

    return query.offset(skip).limit(limit).all()


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


@app.get("/daily-summaries/")
def get_daily_summaries(
        date: datetime.date | None = Query(default=None, description="Filter by date (default: today)"),
        topic_id: int | None = Query(default=None, description="Filter by topic ID"),
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=50, ge=1, le=100),
        session=Depends(get_session_dependency)
) -> list[DailyTrendSummaryList]:
    """
    Fetch daily trend summaries with filtering and pagination.

    - **date**: Filter by specific date (defaults to today)
    - **topic_id**: Filter by topic ID
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (max 100)
    """
    if date is None:
        date = datetime.date.today()

    query = (
        session.query(DailyTrendSummaryDB)
        .options(
            joinedload(DailyTrendSummaryDB.topic),
            joinedload(DailyTrendSummaryDB.articles).joinedload(ArticleDB.topics)
        )
        .filter(DailyTrendSummaryDB.date <= date)
    )

    if topic_id is not None:
        query = query.filter(DailyTrendSummaryDB.topic_id == topic_id)

    query = query.order_by(DailyTrendSummaryDB.date.desc())

    return query.offset(skip).limit(limit).all()
