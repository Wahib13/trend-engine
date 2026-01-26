from db.connection import Base
from db.models import Source, SourceName, Feed, FeedType


def initialise_database(session, default_data):
    session.add_all(default_data)
    session.commit()
