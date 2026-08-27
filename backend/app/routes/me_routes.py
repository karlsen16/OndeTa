from flask import Blueprint
from app.controllers.user_controller import UserController
from app.controllers.post_controller import PostController
from app.controllers.image_controller import ImageController
from flask_jwt_extended import jwt_required

me_bp = Blueprint("me", __name__, url_prefix="/me")


@me_bp.route("", methods=["GET"])
@jwt_required()
def get_my_profile():
    """Retorna os dados do usuário logado (nome, email, etc)."""
    return UserController.get_current_user()

@me_bp.route("", methods=["PATCH"])
@jwt_required()
def update_my_profile():
    """Atualiza dados do perfil (PATCH para alteração parcial)."""
    return UserController.update_current_user()

@me_bp.route("/password", methods=["PATCH"])
@jwt_required()
def update_my_password():
    """Redefine a senha do usuário logado."""
    return UserController.update_password()

# --- MEUS POSTS ---

@me_bp.route("/posts", methods=["GET"])
@jwt_required()
def get_my_posts():
    """Lista todos os posts que pertencem ao usuário logado."""
    return PostController.get_my_posts()

@me_bp.route("/posts/<int:post_id>", methods=["PATCH"])
@jwt_required()
def update_my_post(post_id):
    """Edita um post específico (apenas se pertencer ao usuário)."""
    return PostController.update_my_post(post_id)

# --- IMAGENS DOS MEUS POSTS ---

@me_bp.route("/posts/<int:post_id>/images", methods=["GET"])
@jwt_required()
def get_my_post_images(post_id):
    """Lista imagens de um post específico do usuário."""
    return ImageController.get_post_images(post_id)

@me_bp.route("/posts/<int:post_id>/images", methods=["POST"])
@jwt_required()
def add_image_to_post(post_id):
    """Adiciona uma nova imagem a um post existente."""
    return ImageController.create_image(post_id)

@me_bp.route("/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_my_post_image(image_id):
    """Remove uma imagem específica (DELETE real, como planejado)."""
    return ImageController.delete_image(image_id)