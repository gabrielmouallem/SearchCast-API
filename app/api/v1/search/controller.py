# controller.py
from flask import jsonify, Response
import pymongo
from .dto import SearchDTO
from .service import SearchService

from api.common.utils.utils import format_text_to_double_quotes


class SearchController:
    def __init__(self):
        self.search_service = SearchService()

    def search_transcriptions(self, search: SearchDTO):
        try:
            # Create the text search query
            text_search_query = {
                "$text": {"$search": format_text_to_double_quotes(search.query_text)}
            }

            # Perform the search with pagination
            result_data = self.search_service.search_transcriptions(
                query=text_search_query,
                page=search.page,
                per_page=search.per_page,
            )

            result_count = self.search_service.count_transcriptions(
                query=text_search_query
            )

            response_data = {
                "page": search.page,
                "results": result_data,
                "count": result_count,
            }

            return jsonify(response_data)

        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

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
                {"$sort": {"video.publishDate": pymongo.DESCENDING}},
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
