from flask import Flask
from app.routes.routes import configure_routes
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
