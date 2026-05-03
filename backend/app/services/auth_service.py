from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register(data):
        existing_user = UserRepository.get_by_email(data.get("email"))
        if existing_user:
            raise ValueError("Email já cadastrado")

        hashed_password = generate_password_hash(data.get("password"))

        user = UserRepository.create({
            "name": data.get("name"),
            "email": data.get("email"),
            "password": hashed_password,
            "contact": data.get("contact")
        })

        return user

    @staticmethod
    def login(email, senha):
        user = UserRepository.get_by_email(email)

        if not user:
            raise ValueError("Usuário não encontrado")

        if not check_password_hash(user.password, senha):
            raise ValueError("Senha inválida")

        return user