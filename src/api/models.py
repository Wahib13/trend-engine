from datetime import date
from pydantic import BaseModel


class TopicList(BaseModel):
    id: int
    name: str


class Topic(TopicList):
    articles: list['Article']


class ArticleList(BaseModel):
    id: int
    title: str
    url: str
    topics: list[TopicList]


class Article(ArticleList):
    ...


class DailyTrendSummaryList(BaseModel):
    id: int
    date: date
    summary: str | None
    topic: TopicList
    articles: list[ArticleList]
