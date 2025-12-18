import os

from db.connection import Base
from db.models import Topic, User


def initialise_database(engine, session):
    Base.metadata.create_all(engine)

    default_topic: Topic = Topic(
        description="default topic"
    )
    session.add(default_topic)
    default_user: User = User(
        email=os.environ["DEFAULT_USER_EMAIL"]
    )
    session.add(default_user)
    session.commit()
