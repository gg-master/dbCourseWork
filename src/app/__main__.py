from os import getenv
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", debug=True)
