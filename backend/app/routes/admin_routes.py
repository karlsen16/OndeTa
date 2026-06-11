from flask import Blueprint
from app.controllers.user_controller import UserController
from app.controllers.post_controller import PostController
from app.controllers.image_controller import ImageController
from flask_jwt_extended import jwt_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# --- MODERAÇÃO DE USUÁRIOS ---

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def admin_list_users():
    """Lista todos os usuários (ativos, inativos, banidos)."""
    return UserController.list_users_for_admin()

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def admin_get_user(user_id):
    """Ver detalhes de qualquer usuário."""
    return UserController.get_user_for_admin(user_id)

@admin_bp.route("/users/<int:user_id>", methods=["PATCH"])
@jwt_required()
def admin_update_user(user_id):
    """Banir, tornar admin ou reativar usuário."""
    return UserController.update_user_for_admin(user_id)

# --- MODERAÇÃO DE POSTS ---

@admin_bp.route("/posts", methods=["GET"])
@jwt_required()
def admin_list_posts():
    """Lista todos os posts para auditoria."""
    return PostController.list_posts_for_admin()

@admin_bp.route("/posts/<int:post_id>", methods=["PATCH"])
@jwt_required()
def admin_update_post(post_id):
    """Ocultar post ou mudar categoria/status."""
    return PostController.update_post_for_admin(post_id)

# --- MODERAÇÃO DE IMAGENS ---

@admin_bp.route("/posts/<int:post_id>/images", methods=["GET"])
@jwt_required()
def admin_get_post_images(post_id):
    """Ver todas as imagens de um post, mesmo que oculto."""
    return ImageController.get_post_images(post_id)

@admin_bp.route("/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_image(image_id):
    """Remover imagem permanentemente por violação de termos."""
    return ImageController.delete_image(image_id)