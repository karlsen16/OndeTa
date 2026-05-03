from app.repositories.user_repository import UserRepository
from app.extensions import bcrypt


class UserService:

    @staticmethod
    def get_all_users():

        return UserRepository.get_all()

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError(
                "Usuário não encontrado"
            )

        return user

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError(
                "Usuário não encontrado"
            )

        if "password" in data:
            hashed_password = (
                bcrypt.generate_password_hash(
                    data["password"]
                ).decode("utf-8")
            )
            data["password"] = hashed_password

        return UserRepository.update(user, data)