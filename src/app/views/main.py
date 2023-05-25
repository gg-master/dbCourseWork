from flask import Flask
from .base import main


def register_all_views(app: Flask):
    app.register_blueprint(main.view)
