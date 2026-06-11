from app.extensions import db
from app.models.post import Post
from sqlalchemy import text


class PostRepository:
    @staticmethod
    def create(data):
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def get_paginated_feed(lat, lng, page, limit):
        query = Post.query.filter_by(status="active")

        if lat and lng:
            # Haversine direto no Repository
            haversine = text(
                "(6371 * acos(cos(radians(:lat)) * cos(radians(latitude)) * "
                "cos(radians(longitude) - radians(:lng)) + sin(radians(:lat)) * "
                "sin(radians(latitude))))"
            )
            return query.params(lat=lat, lng=lng) \
                .order_by(haversine.asc(), Post.created_at.desc()) \
                .paginate(page=page, per_page=limit)

        return query.order_by(Post.created_at.desc()).paginate(page=page, per_page=limit)

    @staticmethod
    def update(post, data):
        for key, value in data.items():
            setattr(post, key, value)
        db.session.commit()
        return post