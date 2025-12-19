from db.connection import Base
from db.models import Source, SourceName, Feed, FeedType


def initialise_database(engine, session, default_sources: list[Source]):
    Base.metadata.create_all(engine)

    session.add_all(default_sources)
    session.commit()
