from flask import Flask
from backend import mysql


def create_app():
    app = Flask(__name__, template_folder="html")
    app.config.from_pyfile("config.py")

    mysql.init_app(app)
    import views

    app.add_url_rule("/", view_func=views.login, methods=["POST", "GET"])
    app.add_url_rule("/signup", view_func=views.signup, methods=["POST", "GET"])
    app.add_url_rule("/logout", view_func=views.logout, methods=["POST", "GET"])

    return app
