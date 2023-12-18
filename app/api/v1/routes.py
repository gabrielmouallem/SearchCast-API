# routes.py
from flask import request
from api.common.decorators import requires_auth
from api.v1.search.dto import SearchDTO
from api.v1.search.controller import SearchController


def configure_v1_routes(app):
    @app.route("/v1/search", methods=["GET"], endpoint="search_transcriptions")
    @requires_auth
    def search_transcriptions():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = SearchDTO(query_text, page, per_page)

        return SearchController().search_transcriptions(search=search)

    @app.route(
        "/v1/search_by_video",
        methods=["GET"],
        endpoint="search_transcriptions_by_video",
    )
    @requires_auth
    def search_transcriptions_by_video():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = SearchDTO(query_text, page, per_page)

        return SearchController().search_transcriptions_by_video(search=search)
