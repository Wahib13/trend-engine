import os

from bertopic import BERTopic

import config
import inference.main
from db.connection import get_session
from db.models import User

config.setup_logging()

model = BERTopic()

with get_session() as session:
    user = session.query(User).filter(User.email == os.environ["DEFAULT_USER_EMAIL"]).first()
    if not user:
        raise ValueError(f"user with email: {os.environ['DEFAULT_USER_EMAIL']} not found")
    inference.main.run_clustering(session, model, user)
