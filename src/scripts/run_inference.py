import config
from db.connection import get_session
from inference.main import infer_topics

config.setup_logging()

with get_session() as session:
    infer_topics(session)
