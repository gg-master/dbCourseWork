import logging
from os import getenv
from flask import Flask

from app.views.main import register_all_views
from app.db.implementations import Database


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    # filename=Config.APP_LOG,
    # encoding='utf-8',
)


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    Database.prelaunch_check()

    register_all_views(flask_app)
    # atexit.register(Database.dispose_connection)
    # print(UserRepository(Database).get(1))

    @flask_app.teardown_appcontext
    def close_database_connection(exception=None):
        if exception is not None:
            logging.error('Exception occurred: %s', str(exception))
        Database.dispose_connection()

    return flask_app
