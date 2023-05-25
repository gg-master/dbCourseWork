import logging
import atexit
from os import getenv
from flask import Flask

from app.views.main import register_all_views
from app.db.implementations import Database
from app.db.repositories import UserRepository


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    # filename=Config.APP_LOG,
    # encoding='utf-8',
)


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    register_all_views(flask_app)
    # atexit.register(Database.dispose_connection)
    print(UserRepository(Database).get(1))
    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
