# routes.py
import os
from flask import Response, jsonify, request
from services.mongodb import db
from typing import List, Any
import re

SECRET_KEY = os.environ.get("SECRET_KEY")


def paginate(items: List[Any], page: int, per_page: int) -> List[Any]:
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    return items[start_index:end_index]


def authenticate(api_key):
    """Function to authenticate users based on the provided API key."""
    return api_key == SECRET_KEY


def requires_auth(f):
    """Decorator function to protect routes with authentication."""

    def decorated(*args, **kwargs):
        api_key = request.headers.get("Api-Key")
        if not api_key or not authenticate(api_key):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated


def configure_routes(app):
    @app.route("/search", methods=["GET"])
    @requires_auth
    def search_transcriptions():
        try:
            query_text = request.args.get("text", "")
            page: int = request.args.get("page", 1, type=int)
            per_page: int = request.args.get("per_page", 10, type=int)
            case_sensitive_str: str = request.args.get("caseSensitive", "false")
            exact_text_str: str = request.args.get("exactText", "false")

            # Convert caseSensitive and exactText to boolean values
            case_sensitive: bool = case_sensitive_str.lower() == "true"
            exact_text: bool = exact_text_str.lower() == "true"

            # Create the text search query
            text_search_query = {"$text": {"$search": query_text}}

            # Modify the text search query based on case sensitivity
            if not case_sensitive:
                text_search_query["$text"]["$caseSensitive"] = False

            # If exactText is True, use an exact match query
            if exact_text:
                exact_text_query = {"text": query_text}
            else:
                exact_text_query = {}

            # Combine the text search query and the exact text query
            combined_query = {"$and": [text_search_query, exact_text_query]}

            # Execute the aggregation pipeline
            result_data = list(db.videoTranscriptions.find(combined_query))

            # Filter result_data based on the words in query_text to have all the words included on the final result
            filtered_data = [
                item
                for item in result_data
                if all(
                    word.lower() in item["text"].lower()
                    for word in re.findall(r"\w+", query_text)
                )
            ]

            paginated_data: List[Any] = paginate(filtered_data, page, per_page)

            response_data = {
                "page": page,
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
