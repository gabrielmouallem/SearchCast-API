# service.py
from .repository import SearchRepository


class SearchService:
    def search_transcriptions(self, query, page, per_page):
        return SearchRepository().search_transcriptions(
            query=query, page=page, per_page=per_page
        )

    def count_transcriptions(self, query):
        return SearchRepository().count_transcriptions(query=query)
