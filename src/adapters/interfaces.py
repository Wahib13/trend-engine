from abc import ABC, abstractmethod
from typing import List

from common.hackernews import HackerNewsItem


class HackerNewsAPIInterface(ABC):

    @abstractmethod
    def fetch_hacker_news_items(self, **kwargs) -> List[int]:
        pass

    @abstractmethod
    def fetch_hacker_news_item(self, hacker_news_item_id) -> HackerNewsItem | None:
        pass
