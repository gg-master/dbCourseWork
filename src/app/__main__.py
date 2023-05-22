from os import getenv
from flask import Flask

from views.main import register_all_views


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    register_all_views(app)
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", debug=True)
