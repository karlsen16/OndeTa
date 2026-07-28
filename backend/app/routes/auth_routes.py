from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthController.register()


@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login()


@auth_bp.route("/reactivate", methods=["POST"])
def reactivate():
    return AuthController.login(reactivation=True)