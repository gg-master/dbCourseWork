from flask import Flask
import views.base.main as main


def register_all_views(app: Flask):
    app.register_blueprint(main.view)
