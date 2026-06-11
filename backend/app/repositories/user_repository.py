from app.extensions import db
from app.models import User
from sqlalchemy import select


class UserRepository:

    @staticmethod
    def create(data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email):
        stmt = select(User).filter_by(email=email)
        return db.session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all():
        stmt = select(User)
        return db.session.execute(stmt).scalars().all()

    @staticmethod
    def update(user, data):
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()