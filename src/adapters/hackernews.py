import logging
import types
from typing import List

import requests
from pydantic import TypeAdapter

from adapters.interfaces import HackerNewsAPIInterface
from common.hackernews import HackerNewsItem, Type
from config import HACKER_NEWS_BASE_URL

logger = logging.getLogger(__name__)


class HackerNewsAPIClient(HackerNewsAPIInterface):

    def fetch_hacker_news_items(
            self,
            endpoint="topstories"
    ) -> List[int]:
        response = requests.get(
            f"{HACKER_NEWS_BASE_URL}/{endpoint}.json"
        )
        logger.debug(response.json())
        ids = TypeAdapter(List[int]).validate_python(response.json())
        return ids

    def fetch_hacker_news_item(self, hacker_news_item_id) -> HackerNewsItem | None:
        response = requests.get(
            f"{HACKER_NEWS_BASE_URL}/item/{hacker_news_item_id}.json"
        )
        logger.debug(response.json())
        hn_item = HackerNewsItem.from_json(response.json())

        if hn_item.type == Type.STORY:
            return hn_item
