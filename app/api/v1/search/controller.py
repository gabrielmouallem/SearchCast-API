from flask import jsonify, Response
from .dto import SearchDTO
from .service import SearchService

from api.common.utils.utils import format_text_to_double_quotes


class SearchController:
    def __init__(self):
        self.search_service = SearchService()

    def search_transcriptions_by_video(self, search: SearchDTO):
        try:
            skip_count = (search.page - 1) * search.per_page

            common_pipeline = [
                {
                    "$match": {
                        "$text": {
                            "$search": format_text_to_double_quotes(search.query_text)
                        }
                    }
                },
                {"$addFields": {"video.viewCount": {"$toInt": "$video.viewCount"}}},
                {
                    "$group": {
                        "_id": "$video._id",
                        "transcriptions": {
                            "$push": {
                                "text": "$text",
                                "start": "$start",
                                "duration": "$duration",
                            }
                        },
                        "video": {"$first": "$video"},
                    }
                },
            ]

            # Aggregation for expanded transcription within each transcription
            expanded_transcription_stage = {
                "$lookup": {
                    "from": "videoTranscriptions",  # Assuming collection name is videoTranscriptions
                    "let": {"videoId": "$video.videoId", "startTime": "$start"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$video.videoId", "$$videoId"]},
                                        {
                                            "$gt": [
                                                "$start",
                                                {"$subtract": ["$$startTime", 10]},
                                            ]
                                        },
                                        {
                                            "$lt": [
                                                "$start",
                                                {"$add": ["$$startTime", 10]},
                                            ]
                                        },
                                    ]
                                }
                            }
                        },
                        {"$sort": {"start": 1}},
                        {
                            "$group": {
                                "_id": "$video.videoId",
                                "merged_start": {"$first": "$start"},
                                "merged_end": {
                                    "$last": {"$add": ["$start", "$duration"]}
                                },
                                "merged_text": {"$push": "$text"},
                                "merged_duration": {"$sum": "$duration"},
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "start": "$merged_start",
                                "end": "$merged_end",
                                "text": {
                                    "$reduce": {
                                        "input": "$merged_text",
                                        "initialValue": "",
                                        "in": {"$concat": ["$$value", " ", "$$this"]},
                                    }
                                },
                                "duration": "$merged_duration",
                            }
                        },
                    ],
                    "as": "expanded_transcription",
                }
            }

            # Create the text search query
            results_pipeline = common_pipeline + [
                {"$unwind": "$transcriptions"},
                {"$addFields": {"start": "$transcriptions.start"}},
                expanded_transcription_stage,
                {"$sort": search.order_by},
                {"$skip": skip_count},
                {"$limit": search.per_page},
                {
                    "$group": {
                        "_id": None,
                        "results": {"$push": "$$ROOT"},
                    }
                },
                {"$project": {"_id": 0, "results": 1, "count": 1}},
            ]

            count_pipeline = common_pipeline + [
                {
                    "$count": "count",
                },
            ]

            # Perform the search with pagination
            result_data = self.search_service.aggregate_transcriptions(
                pipeline=results_pipeline
            )

            count_data = self.search_service.aggregate_transcriptions(
                pipeline=count_pipeline
            )

            response_data = {
                **result_data,
                **count_data,
                "page": search.page,
            }

            return jsonify(response_data)

        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )
