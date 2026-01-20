import config
from adapters.ollama import OllamaClient
from db.connection import get_session
from summary.main import generate_article_summaries

config.setup_logging()

with get_session() as session:
    generate_article_summaries(session, OllamaClient(config.settings.OLLAMA_MODEL))
