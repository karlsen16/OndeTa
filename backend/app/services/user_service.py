from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def update_password(user_id, current_password, new_password):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        if not check_password_hash(user.password, current_password):
            raise ValueError("Senha atual incorreta")

        hashed = generate_password_hash(new_password)
        UserRepository.update_password(user, hashed)

    @staticmethod
    def delete_account(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        UserRepository.delete(user)
