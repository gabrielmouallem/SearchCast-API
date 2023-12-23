# routes.py
from flask import request
from api.common.decorators import requires_auth, requires_payment
from api.v1.search.dto import SearchDTO
from api.v1.search.controller import SearchController
from api.v1.auth.controller import UserController
from api.v1.auth.dto import LoginDTO, UserDTO


def configure_v1_routes(app):
    @app.route("/v1/search", methods=["GET"], endpoint="search_transcriptions")
    @requires_auth
    @requires_payment
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
    @requires_payment
    def search_transcriptions_by_video():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = SearchDTO(query_text, page, per_page)

        return SearchController().search_transcriptions_by_video(search=search)

    @app.route(
        "/v1/login",
        methods=["POST"],
        endpoint="login",
    )
    def login():
        json = request.get_json()
        email = json["email"]
        password = json["password"]

        login = LoginDTO(email, password)

        return UserController().login(login=login)

    @app.route(
        "/v1/register",
        methods=["POST"],
        endpoint="register",
    )
    def register():
        json = request.get_json()
        name = json["name"]
        email = json["email"]
        password = json["password"]

        register = UserDTO(name, email, password)

        return UserController().register(register=register)
