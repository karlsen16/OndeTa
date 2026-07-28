from app.extensions import db
from app.models import Post
from sqlalchemy import func
from sqlalchemy.orm import joinedload, load_only


class PostRepository:
    @staticmethod
    def _apply_query_options(query, lean):
        if lean:
            return query.options(
                load_only(
                    Post.id,
                    Post.pet_type,
                    Post.category,
                    Post.status,
                    Post.latitude,
                    Post.longitude
                )
            )
        else:
            return query.options(joinedload(Post.images))

    @staticmethod
    def create(data):
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_post(post_id, lean=False):
        query = db.session.query(Post)

        query = PostRepository._apply_query_options(query, lean)
        query = query.filter(Post.id == post_id)

        return query.first()

    @staticmethod
    def get_feed(params, lean=False):
        query = db.session.query(Post)

        query = PostRepository._apply_query_options(query, lean)

        if params.get("pet_type"):
            query = query.filter(Post.pet_type == params["pet_type"])

        if params.get("category"):
            query = query.filter(Post.category == params["category"])

        if "allowed_statuses" in params:
            query = query.filter(Post.status.in_(params["allowed_statuses"]))

        lat = params.get("latitude")
        lng = params.get("longitude")
        distance_limit = params.get("distance")

        haversine_distance = (
                6371 * func.acos(
            func.cos(func.radians(lat)) * func.cos(func.radians(Post.latitude)) * func.cos(
                func.radians(Post.longitude) - func.radians(lng)) +
            func.sin(func.radians(lat)) * func.sin(func.radians(Post.latitude))
            )
        )

        query = query.filter(haversine_distance <= distance_limit)
        query = query.order_by(haversine_distance.asc(), Post.created_at.desc())
        total_posts = query.count()

        limit = params.get("limit")
        if not lean:
            page = params.get("page")
            offset = (page - 1) * limit
            posts = query.offset(offset).limit(limit).all()
        else:
            posts = query.limit(limit).all()

        return total_posts, posts

    @staticmethod
    def update(post, data):
        for key, value in data.items():
            setattr(post, key, value)
        db.session.commit()
        return post