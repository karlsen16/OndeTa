from flask import Blueprint
from app.controllers.post_controller import PostController
from flask_jwt_extended import jwt_required

post_bp = Blueprint("posts", __name__, url_prefix="/posts")


@post_bp.route("", methods=["GET"])
def get_feed():
    """
        Retorna o feed de posts.
        Query params esperados: page, limit, lat, lng
        """
    return PostController.get_feed()


@post_bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    """
    Cria um novo post.
    O user_id será extraído do token pelo Controller.
    """
    return PostController.create_post()


@post_bp.route("/<int:post_id>", methods=["GET"])
def get_by_id(post_id):
    """
    Retorna os detalhes de um post específico.
    Útil para quando o usuário clica em um pin no mapa.
    """
    return PostController.get_by_id(post_id)