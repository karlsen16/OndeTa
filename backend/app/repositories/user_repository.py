from app.extensions import db
from app.models import User
from sqlalchemy.orm import joinedload, load_only


class UserRepository:
    @staticmethod
    def _apply_query_options(query, include_assets, lean):
        if lean:
            return query.options(
                load_only(
                    User.id,
                    User.status,
                    User.role
                )
            )
        elif include_assets:
            return query.options(joinedload(User.posts))

        return query

    @staticmethod
    def create(data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user


    @staticmethod
    def get_user(user_id=None, email=None, include_assets=False, lean=False):
        query = db.session.query(User)

        query = UserRepository._apply_query_options(query, include_assets, lean)

        if user_id is not None:
            query = query.filter(User.id == user_id)
        elif email is not None:
            query = query.filter(User.email == email)
        else:
            return None

        return query.first()

    @staticmethod
    def get_feed(params, include_assets=False, lean=False):
        query = db.session.query(User)

        query = UserRepository._apply_query_options(query, include_assets, lean)

        if params.get("status"):
            query = query.filter(User.status == params["status"])

        if params.get("role"):
            query = query.filter(User.role == params["role"])

        order = params.get("order", None)
        if order == "newest":
            query = query.order_by(User.created_at.desc())
        elif order == "oldest":
            query = query.order_by(User.created_at.asc())
        else:
            query = query.order_by(User.updated_at.desc())
        total_users = query.count()

        limit = params.get("limit")
        page = params.get("page")
        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()

        return total_users, users

    @staticmethod
    def update(user, data):
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user