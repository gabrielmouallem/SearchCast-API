# routes.py
from flask import Response, request
from api.common.decorators import requires_auth, requires_payment
from api.v1.search.dto import SearchDTO
from api.v1.search.controller import SearchController
from api.v1.auth.controller import UserController
from api.v1.auth.dto import GoogleLoginDTO, GoogleResponseDTO, PasswordLoginDTO, UserDTO


def configure_v1_routes(app):
    @app.route("/v1/search", methods=["GET"], endpoint="search_transcriptions")
    @requires_auth
    @requires_payment
    def search_transcriptions():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = SearchDTO(query_text, page, per_page)

        try:
            return SearchController().search_transcriptions(search=search)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

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

        try:
            return SearchController().search_transcriptions_by_video(search=search)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/login",
        methods=["POST"],
        endpoint="login",
    )
    def login():
        json = request.get_json()
        email = json["email"]
        password = json["password"]

        login = PasswordLoginDTO(email, password)

        try:
            return UserController().password_login(login=login)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/google_login",
        methods=["POST"],
        endpoint="google_login",
    )
    def google_login():
        json = request.get_json()
        googleId = json["googleId"]
        imageUrl = json["imageUrl"]
        email = json["email"]
        name = json["name"]
        givenName = json["givenName"]
        familyName = json["familyName"]

        raw_google_response = json["google_response"]

        token_type = raw_google_response["token_type"]
        access_token = raw_google_response["access_token"]
        scope = raw_google_response["scope"]
        login_hint = raw_google_response["login_hint"]
        expires_in = raw_google_response["expires_in"]
        id_token = raw_google_response["id_token"]
        session_state = raw_google_response["session_state"]
        first_issued_at = raw_google_response["first_issued_at"]
        expires_at = raw_google_response["expires_at"]
        idpId = raw_google_response["idpId"]

        google_response = GoogleResponseDTO(
            token_type,
            access_token,
            scope,
            login_hint,
            expires_in,
            id_token,
            session_state,
            first_issued_at,
            expires_at,
            idpId,
        )

        login = GoogleLoginDTO(
            googleId,
            imageUrl,
            email,
            name,
            givenName,
            familyName,
            google_response,
        )

        # try:
        return UserController().google_login(login=login)
        # except Exception as e:
        #     return Response(
        #         response=str(e),
        #         status=500,
        #         mimetype="application/json",
        #     )

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

        try:
            return UserController().register_w_password(register=register)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )
