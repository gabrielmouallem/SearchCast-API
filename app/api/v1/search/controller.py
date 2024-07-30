from flask import jsonify, Response
from .dto import SearchDTO
from .service import SearchService

from api.common.utils.utils import format_text_to_double_quotes


class SearchController:
    def __init__(self):
        self.search_service = SearchService()

    def search_transcriptions_by_video(self, search: SearchDTO):
        try:
            print(search.order_by)
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
            # Create the text search query
            results_pipeline = common_pipeline + [
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

    def expanded_transcription(self, video_id, start_time):

        # Aggregation pipeline to find 2 before and 2 after the target transcription
        pipeline = [
            {
                "$match": {
                    "video._id": video_id,
                    "start": {"$gt": start_time - 10, "$lt": start_time + 10},
                }
            },
            {"$sort": {"start": 1}},  # Ensure documents are sorted by start time
            {
                "$group": {
                    "_id": "$video._id",  # Grouping by videoId, adjust if you need different granularity
                    "merged_start": {"$first": "$start"},
                    "merged_end": {"$last": {"$add": ["$start", "$duration"]}},
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
        ]

        transcriptions = self.search_service.aggregate_transcriptions(pipeline=pipeline)
        if len(transcriptions) > 0:
            return jsonify(transcriptions)
        return (
            jsonify({"error": "No transcriptions found or error in aggregation"}),
            404,
        )
