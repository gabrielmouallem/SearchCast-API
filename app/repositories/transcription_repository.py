from app.services.mongodb.mongodb_service import db


class TranscriptionRepository:
    def __init__(self):
        self.db = db

    def search_transcriptions(self, query):
        # Execute the aggregation pipeline
        return list(self.db.videoTranscriptions.find(query))
