# routes.py
from flask import jsonify
from api.v1.routes import configure_v1_routes


def configure_routes(app):
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"message": "Server is online!"})

    configure_v1_routes(app)
