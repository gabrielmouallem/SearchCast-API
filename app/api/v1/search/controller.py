# controller/search_controller.py
from flask import jsonify, Response
from .dto import SearchDTO
from .service import SearchService

from api.common.utils.utils import paginate


class SearchController:
    def __init__(self):
        self.search_service = SearchService()

    def search_transcriptions(self, search: SearchDTO):
        try:
            # Create the text search query
            text_search_query = {"$text": {"$search": search.query_text}}

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

            # Perform the search and sort using the aggregation pipeline
            result_data = self.search_service.search_transcriptions(
                query=combined_query
            )

            filtered_data = self.search_service.filter_data(
                result_data, search.query_text
            )

            paginated_data = paginate(filtered_data, search.page, search.per_page)

            response_data = {
                "page": search.page,
                "results": paginated_data,
                "count": len(filtered_data),
            }

            return jsonify(response_data)

        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )
