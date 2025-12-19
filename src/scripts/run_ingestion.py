import config
from db.connection import get_session
from ingestion.main import save_articles, fetch_rss_entries

config.setup_logging()

with get_session() as session:
    new_articles = fetch_rss_entries(session)
    save_articles(new_articles, session)
