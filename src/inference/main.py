import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.topic import Topic
from db.models import Article as ArticleModel
from db.models import Topic as TopicModel

logger = logging.getLogger(__name__)


def get_topic(model, story):
    topic_ids, probabilities = model.transform(story.title)
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
):
    db_stories = session.query(ArticleModel).all()
    for story in db_stories:
        topic_ = get_topic(model, story)
        logger.info(f"found topic: {topic_}")
        topic = get_or_create_db_topic(session, topic_)
        if topic not in story.topics:
            story.topics.append(topic)

    session.commit()


def run_clustering(
        session: Session,
        model,
):
    """
    trains a new version of the model on the entire ingested story titles and runs inference on each of them
    to cluster them into topics
    :return:
    """
    model = retrain(session, model)
    run_inference(
        model,
        session
    )
