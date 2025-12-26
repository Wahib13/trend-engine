import logging

from newspaper import Article

import config
from db.models import Article as ArticleDB

from db.connection import get_session

config.setup_logging()

logger = logging.getLogger(__name__)

with get_session() as session:
    articles = session.query(ArticleDB)
    for article in articles:
        try:
            url = article.url

            if not article.text:
                newspaper_article = Article(url)
                newspaper_article.download()
                newspaper_article.parse()

                text = newspaper_article.text
                title = newspaper_article.title

                article.text = text
                session.commit()

                logger.debug(f"processed article {article.id}.database title: {article.title} | extracted title: {title}")
        except Exception as e:
            logger.warning(f"error when parsing article: {article.id}: {str(e)}")
