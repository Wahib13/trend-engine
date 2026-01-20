import config
from adapters.ollama import OllamaClient
from db.connection import get_session
from summary.main import generate_daily_summary

config.setup_logging()

with get_session() as session:
    generate_daily_summary(session, OllamaClient(config.settings.OLLAMA_MODEL))
