# routes.py
from flask import request
from api.common.decorators import requires_auth
from api.v1.search.dto import SearchDTO
from api.v1.search.controller import SearchController


def configure_v1_routes(app):
    @app.route("/v1/search", methods=["GET"])
    @requires_auth
    def search_transcriptions():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        case_sensitive_str = request.args.get("caseSensitive", "false")
        exact_text_str = request.args.get("exactText", "false")

        # Convert caseSensitive and exactText to boolean values
        case_sensitive = case_sensitive_str.lower() == "true"
        exact_text = exact_text_str.lower() == "true"

        search = SearchDTO(query_text, page, per_page, case_sensitive, exact_text)

        return SearchController().search_transcriptions(search=search)
