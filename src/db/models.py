import datetime

from sqlalchemy import Column, Integer, DateTime, String, Text, JSON, ForeignKey, Date, Table
from sqlalchemy.orm import relationship

from db.connection import Base

article_topic = Table(
    "article_topic",
    Base.metadata,
    Column("article_id", ForeignKey("article.id"), primary_key=True),
    Column("topic_id", ForeignKey("topic.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)
    category = Column(String, nullable=True)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    articles = relationship("Article", secondary=article_topic, back_populates="topics")


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)

    daily_trend_summary_id = Column(Integer, ForeignKey("daily_trend_summary.id"), nullable=True)
    daily_trend_summary = relationship("DailyTrendSummary", back_populates="articles")

    comments = relationship("Comment", cascade="all, delete", order_by="Comment.id")

    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    source_topic = Column(String, nullable=True) # the topic that the source website gave this article. nullable because some sources may not have it.
    author = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    num_comments = Column(Integer, nullable=True)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    sentiment = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)

    topics = relationship("Topic", secondary=article_topic, back_populates="articles")


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    article = relationship("Article", back_populates="comments")

    author = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    sentiment = Column(JSON, nullable=True)
    topics = Column(JSON, nullable=True)


class DailyTrendSummary(Base):
    __tablename__ = 'daily_trend_summary'

    id = Column(Integer, primary_key=True)

    date = Column(Date, nullable=False)
    summary = Column(Text, nullable=True)
    dominant_topics = Column(JSON, nullable=True)
    predicted_trends = Column(JSON, nullable=True)

    articles = relationship("Article", back_populates="daily_trend_summary")
