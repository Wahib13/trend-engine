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


class Article(ArticleList):
    topics: list[TopicList]
