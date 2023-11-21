# routes.py
from flask import jsonify, request
from pymongo import MongoClient
from typing import List, Any

client = MongoClient("mongodb://localhost:27017")
db = client.shortsSniper


def paginate(items: List[Any], page: int, per_page: int) -> List[Any]:
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    return items[start_index:end_index]


def configure_routes(app):
    @app.route("/videoData", methods=["GET"])
    def get_all_video_data():
        videoDatas = db.videoData.find()
        return jsonify([data for data in videoDatas])

    @app.route("/videoData/<int:id>", methods=["GET"])
    def get_video_data_by_id(id):
        videoData = db.videoData.find_one({"_id": id})
        return videoData

    @app.route("/search", methods=["GET"])
    def search_transcriptions():
        query_text = request.args.get("text", "")
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 10, type=int)

        # Perform case-insensitive regex search on the 'text' field
        regex_query = {"text": {"$regex": f".*{query_text}.*", "$options": "i"}}

        # Aggregation pipeline to join videoData with matching videoTranscriptions
        aggregation_pipeline = [
            {"$match": regex_query},
            {
                "$lookup": {
                    "from": "videoData",
                    "localField": "videoId",
                    "foreignField": "_id",
                    "as": "videoData",
                }
            },
            {"$unwind": "$videoData"},
            {"$project": {"_id": 0, "transcription": "$$ROOT"}},
        ]

        # Execute the aggregation pipeline
        aggregated_data = list(db.videoTranscriptions.aggregate(aggregation_pipeline))

        paginated_data: List[Any] = paginate(aggregated_data, page, per_page)

        return jsonify(paginated_data)
