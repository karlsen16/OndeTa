from flask import Blueprint
from app.controllers.post_controller import PostController

post_bp = Blueprint("posts", __name__, url_prefix="/posts")


@post_bp.route("", methods=["GET"])
def get_feed():
    return PostController.get_feed()


@post_bp.route("/pins", methods=["GET"])
def get_pins():
    return PostController.get_pins()


@post_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    return PostController.get_post(post_id)