from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.post_service import PostService
from app.schemas.post_schema import PostResponseSchema, PostCreateSchema, PostUpdateSchema


class PostController:

    # --- PÚBLICO (/posts) ---

    @staticmethod
    def get_feed():
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        pagination = PostService.get_hybrid_feed(lat, lng, page, limit)

        return jsonify({
            "posts": PostResponseSchema(many=True).dump(pagination.items),
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }), 200

    @staticmethod
    def create_post():
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validação de entrada
        errors = PostCreateSchema().validate(data)
        if errors:
            return jsonify(errors), 400

        new_post = PostService.create_post(data, user_id)
        return PostResponseSchema().dump(new_post), 201

    @staticmethod
    def get_by_id(post_id):
        post = PostService.get_post_or_404(post_id)
        return PostResponseSchema().dump(post), 200

    # --- CONTEXTO USUÁRIO LOGADO (/me/posts) ---

    @staticmethod
    def get_my_posts():
        user_id = get_jwt_identity()
        posts = PostService.get_posts_by_user(user_id)
        return PostResponseSchema(many=True).dump(posts), 200

    @staticmethod
    def update_my_post(post_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        errors = PostUpdateSchema().validate(data)
        if errors:
            return jsonify(errors), 400

        updated_post = PostService.update_post_safe(post_id, user_id, data)
        return PostResponseSchema().dump(updated_post), 200

    # --- MAPA (/map) ---

    @staticmethod
    def get_map_pins():
        # Retorna apenas o essencial para performance
        pins = PostService.get_all_active_pins()
        # Aqui poderíamos usar um schema simplificado se preferir
        return jsonify(pins), 200

    @staticmethod
    def get_map_view():
        highlight_id = request.args.get('highlight', type=int)
        data = PostService.get_map_context(highlight_id)
        return jsonify(data), 200

    # --- ADMIN (/admin/posts) ---

    @staticmethod
    def list_posts_for_admin():
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)

        pagination = PostService.get_all_posts_admin(page, limit)
        return jsonify({
            "posts": PostResponseSchema(many=True).dump(pagination.items),
            "total": pagination.total
        }), 200

    @staticmethod
    def update_post_for_admin(post_id):
        data = request.get_json()
        # Admin usa o mesmo schema de update, mas o service ignora a trava de "dono"
        updated_post = PostService.update_post_admin(post_id, data)
        return PostResponseSchema().dump(updated_post), 200