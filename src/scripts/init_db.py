from db.connection import engine, get_session
from db.initialise import initialise_database
from db.models import Source, SourceName, FeedType, Feed

if __name__ == "__main__":
    with get_session() as session:
        source_bbc = Source(name=SourceName.BBC)
        source_the_guardian = Source(name=SourceName.THE_GUARDIAN)
        source_bbc.feeds = [
            Feed(url="https://feeds.bbci.co.uk/news/politics/rss.xml", feed_type=FeedType.POLITICS),
            Feed(url="https://feeds.bbci.co.uk/news/technology/rss.xml", feed_type=FeedType.TECHNOLOGY),
            Feed(url="https://feeds.bbci.co.uk/news/business/rss.xml", feed_type=FeedType.BUSINESS),
            Feed(url="https://feeds.bbci.co.uk/news/health/rss.xml", feed_type=FeedType.HEALTH)
        ]
        source_the_guardian.feeds = [
            Feed(url="https://www.theguardian.com/politics/rss", feed_type=FeedType.POLITICS),
            Feed(url="https://www.theguardian.com/technology/rss", feed_type=FeedType.TECHNOLOGY),
            Feed(url="https://www.theguardian.com/business/rss", feed_type=FeedType.BUSINESS),
            Feed(url="https://www.theguardian.com/society/health/rss", feed_type=FeedType.HEALTH)
        ]
        initialise_database(engine, session, [source_bbc, source_the_guardian])
