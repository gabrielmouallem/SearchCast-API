# service.py
import re
from .repository import SearchRepository


def get_publish_date(item):
    return item["video"]["publishDate"]


class SearchService:
    def search_transcriptions(self, query, page, per_page):
        return SearchRepository().search_transcriptions(
            query=query, page=page, per_page=per_page
        )

    def count_transcriptions(self, query):
        return SearchRepository().count_transcriptions(query=query)
