from bertopic import BERTopic

import config
import inference.main
from db.connection import get_session

config.setup_logging()

model = BERTopic()

with get_session() as session:
    inference.main.run_clustering(session, model)
