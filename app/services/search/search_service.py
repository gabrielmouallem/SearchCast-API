import re

from app.repositories.transcription_repository import TranscriptionRepository


class SearchService:
    def search_transcriptions(self, query):
        return TranscriptionRepository().search_transcriptions(query=query)

    def filter_data(self, result_data, query_text):
        return [
            item
            for item in result_data
            if all(
                word.lower() in item["text"].lower()
                for word in re.findall(r"\w+", query_text)
            )
        ]
