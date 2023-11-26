from flask import Flask
from app.routes import configure_routes
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True

configure_routes(app)
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
