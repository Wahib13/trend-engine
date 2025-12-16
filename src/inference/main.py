import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.topic import Topic
from db.models import Article as ArticleModel, User, UserArticleTopic
from db.models import Topic as TopicModel

logger = logging.getLogger(__name__)


def get_topic(model, article):
    topic_ids, probabilities = model.transform(article.title)
    topic = model.get_topic_info(topic_ids[0]).iloc[0]
    return Topic(
        id=topic.Topic,
        name=topic.Name,
        representation=topic.Representation,
        representative_docs=topic.Representative_Docs,
    )


def get_or_create_db_topic(
        session: Session,
        topic: Topic
):
    db_topic = session.query(TopicModel).filter(TopicModel.id == topic.id).first()
    if not db_topic:
        db_topic = TopicModel(
            id=topic.id,
            description=topic.name,
            keywords={"representation": topic.representation, "repr_docs": topic.representative_docs}
        )
    return db_topic


def retrain(
        session: Session,
        model,
):
    titles = session.execute(
        select(ArticleModel.title)
    ).scalars().all()
    model.fit(titles)
    return model


def run_inference(
        model,
        session: Session,
        user: User
):
    db_articles = session.query(ArticleModel).all()
    for article in db_articles:
        topic_ = get_topic(model, article)
        logger.info(f"found topic: {topic_}")
        topic = get_or_create_db_topic(session, topic_)

        user_topics_for_article = [
            user_article.topic
            for user_article in user.article_topics
            if user_article.article_id == article.id
        ]

        if topic not in user_topics_for_article:
            article_topic = UserArticleTopic(
                user=user,
                topic=topic,
                article=article,
            )
            user.article_topics.append(article_topic)

    session.commit()


def run_clustering(
        session: Session,
        model,
        user: User
):
    """
    trains a new version of the model on the entire ingested article titles and runs inference on each of them
    to cluster them into topics
    :return:
    """

    model = retrain(session, model)
    run_inference(
        model,
        session,
        user
    )
