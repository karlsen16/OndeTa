import math
from app.repositories.post_repository import PostRepository
from app.utils.exceptions import NotFoundError, DensityLimitError


class PostService:
    @staticmethod
    def _prepare_allowed_statuses(params):
        if params.get("status"):
            params["allowed_statuses"] = [params.get("status")]
        else:
            params["allowed_statuses"] = ["active", "resolved"]
        return params

    @staticmethod
    def get_feed(params):
        params = PostService._prepare_allowed_statuses(params)
        page = params.get("page")
        limit = params.get("limit")

        total_posts, posts = PostRepository.get_feed(params)
        total_pages = math.ceil(total_posts / limit) if total_posts > 0 else 1

        pagination_metadata = {
            "current_page": page,
            "limit": limit,
            "total_posts": total_posts,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

        return pagination_metadata, posts

    @staticmethod
    def get_pins(params):
        params = PostService._prepare_allowed_statuses(params)
        total_pins, pins = PostRepository.get_feed(params, lean=True)

        if total_pins > 200:
            raise DensityLimitError("Limite de pins atingido.")

        return pins

    @staticmethod
    def create_post(data, user_id):
        return PostRepository.create({**data, "user_id": user_id})

    @staticmethod
    def get_post(post_id, user=None):
        post = PostRepository.get_post(post_id)

        authorized_user = False
        if (user is not None) and (
            ((post is not None and post.user_id == user.id) or
              getattr(user, "role", None) == "admin")):
            authorized_user = True

        if not post or (post.status in ["hidden", "blocked"] and not authorized_user):
            raise NotFoundError("Post não encontrado.")

        return post