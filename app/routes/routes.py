# routes.py
from flask import jsonify, request
from app.controllers.search_controller import SearchController
from app.decorators.requires_auth import requires_auth
from app.dtos.search_dto import SearchDTO


def configure_routes(app):
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"message": "Server is online!"})

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
