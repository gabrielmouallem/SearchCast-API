import re

from api.v1.search.repository import SearchRepository


def get_publish_date(item):
    return item["video"]["publishDate"]


class SearchService:
    def search_transcriptions(self, query):
        return SearchRepository().search_transcriptions(query=query)

    def sort_data(self, result_data):
        try:
            return sorted(result_data, key=get_publish_date, reverse=True)
        except:
            return result_data

    def filter_data(self, result_data, query_text):
        return [
            item
            for item in result_data
            if all(
                word.lower() in item["text"].lower()
                for word in re.findall(r"\w+", query_text)
            )
        ]
