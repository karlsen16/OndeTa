from flask import Blueprint
from app.controllers.user_controller import UserController

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["GET"])
def get_all_users():
    return UserController.get_all_users()


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    return UserController.get_user_by_id(user_id)