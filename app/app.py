from flask import Flask
from routes import configure_routes

app = Flask(__name__)
app.config["DEBUG"] = True

configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
