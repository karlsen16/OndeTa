from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.exceptions import ForbiddenError, UnauthorizedError, ConflictError
from app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def _ensure_user_exists(user):
        if user is None:
            raise UnauthorizedError

    @staticmethod
    def _check_status_policy(status, allowed_status="active", raise_on_conflict=None):
        if status == allowed_status:
            return

        if raise_on_conflict and status == raise_on_conflict:
            raise ConflictError(f"Operação inválida. O usuário está com status '{status}'.")

        if status == "banned":
            raise ForbiddenError("Acesso negado. Sua conta está banida.")

        raise ForbiddenError(f"Acesso negado. Sua conta está desativada.")


    @staticmethod
    def _check_password(stored_password_hash, provided_password):
        if not check_password_hash(stored_password_hash, provided_password):
            raise UnauthorizedError


    @staticmethod
    def _generate_token(user, ip_address):
        return create_access_token(
            identity=str(user.id),
            additional_claims= {
                "role": user.role,
                "ip": ip_address
            }
        )


    @staticmethod
    def _check_email_availability(email):
        existing_user = UserRepository.get_user(email=email, lean=True)

        if existing_user is not None:
            raise ConflictError("E-mail já cadastrado no sistema.")


    @staticmethod
    def get_aa_user(user_id, user_role, admin_required, include_assets, lean):
        user = UserRepository.get_user(user_id=user_id, include_assets=include_assets, lean=lean)
        AuthService._ensure_user_exists(user)

        if user_role != user.role:
            raise ForbiddenError("Acesso negado. Credenciais corrompidas.")

        if admin_required and user_role != "admin":
            raise ForbiddenError

        AuthService._check_status_policy(user.status)
        return user


    @staticmethod
    def register(data, ip_address):
        AuthService._check_email_availability(data.get("email"))

        hashed_password = generate_password_hash(data.get("password"))
        user = UserRepository.create({
            "name": data.get("name"),
            "email": data.get("email"),
            "password": hashed_password,
            "contact": data.get("contact")
        })

        return AuthService._generate_token(user, ip_address), user


    @staticmethod
    def login(data, ip_address, reactivation):
        user = UserRepository.get_user(email=data.get("email"))
        AuthService._ensure_user_exists(user)
        AuthService._check_password(user.password, data.get("password"))
        if reactivation:
            AuthService._check_status_policy(user.status, allowed_status="inactive", raise_on_conflict="active")
            user = UserRepository.update(user, {"status":"active"})
        else:
            AuthService._check_status_policy(user.status, raise_on_conflict="inactive")
        return AuthService._generate_token(user, ip_address), user