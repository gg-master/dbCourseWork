from flask import Flask
from .base import main as base_main
from .admin import main as admin_main


def register_all_views(app: Flask):
    app.register_blueprint(base_main.view)
    app.register_blueprint(admin_main.view)
