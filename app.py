from flask import Flask
from backend import mysql
import os


def create_app():
    app = Flask(__name__, template_folder="html")
    app.config.from_pyfile("config.py")

    mysql.init_app(app)

    # Ensure the upload directory exists
    os.makedirs(app.config["UPLOADS_FOLDER"], exist_ok=True)

    import views

    # Standard
    app.add_url_rule("/", view_func=views.index, methods=["POST", "GET"])
    app.add_url_rule("/login", view_func=views.login, methods=["POST", "GET"])
    app.add_url_rule("/signup", view_func=views.signup, methods=["POST", "GET"])
    app.add_url_rule("/logout", view_func=views.logout, methods=["POST", "GET"])
    app.add_url_rule(
        "/edit_profile", view_func=views.edit_profile, methods=["POST", "GET"]
    )
    app.add_url_rule("/dashboard", view_func=views.dashboard, methods=["POST", "GET"])

    # Requester-related
    app.add_url_rule(
        "/book_request", view_func=views.book_request, methods=["POST", "GET"]
    )
    app.add_url_rule(
        "/cancel_request", view_func=views.cancel_request, methods=["POST", "GET"]
    )
    app.add_url_rule(
        "/confirm_request", view_func=views.confirm_request, methods=["POST", "GET"]
    )

    # Uploader-related
    app.add_url_rule("/upload", view_func=views.upload, methods=["POST", "GET"])
    app.add_url_rule(
        "/delete_upload", view_func=views.delete_upload, methods=["POST", "GET"]
    )
    app.add_url_rule(
        "/accept_request", view_func=views.accept_request, methods=["POST", "GET"]
    )

    return app
