# repository.py
from api.common.services.mongodb import db


class SearchRepository:
    def __init__(self):
        self.db = db

    def search_transcriptions(self, query, page=1, per_page=10):
        # Calculate skip count based on pagination parameters
        skip_count = (page - 1) * per_page

        # Execute the aggregation pipeline with pagination
        result_data = (
            self.db.videoTranscriptions.find(query).skip(skip_count).limit(per_page)
        )

        return list(result_data)

    def count_transcriptions(self, query):
        # Execute a count query
        return self.db.videoTranscriptions.count_documents(query)
