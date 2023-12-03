# controller.py
from flask import jsonify, Response
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

            # Modify the text search query based on case sensitivity
            if not search.case_sensitive:
                text_search_query["$text"]["$caseSensitive"] = False

            # If exactText is True, use an exact match query
            if search.exact_text:
                exact_text_query = {"text": search.query_text}
            else:
                exact_text_query = {}

            # Combine the text search query and the exact text query
            combined_query = {"$and": [text_search_query, exact_text_query]}

            # Perform the search with pagination
            result_data = self.search_service.search_transcriptions(
                query=combined_query,
                page=search.page,
                per_page=search.per_page,
            )

            result_count = self.search_service.count_transcriptions(
                query=combined_query
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
