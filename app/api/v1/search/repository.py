# repository.py
import pymongo
from api.common.services.mongodb import get_db


class SearchRepository:
    def __init__(self):
        self.db = get_db()

    def search_transcriptions(self, query, page=1, per_page=10):
        # Calculate skip count based on pagination parameters
        skip_count = (page - 1) * per_page

        # Execute the aggregation pipeline with pagination
        result_data = (
            self.db.videoTranscriptions.find(query)
            .sort("video.publishDate", pymongo.DESCENDING)
            .skip(skip_count)
            .limit(per_page)
        )

        return list(result_data)

    def count_transcriptions(self, query):
        # Execute a count query
        return self.db.videoTranscriptions.count_documents(query)

    def aggregate_transcriptions(self, pipeline):
        result = list(self.db.videoTranscriptions.aggregate(pipeline))
        return result[0] if result else {}
