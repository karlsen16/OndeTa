from app.extensions import db
from app.models.user import User
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import UnauthorizedError


class UserService:

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def update_password(user, old_password, new_password):
        if not check_password_hash(user.password, old_password):
            raise UnauthorizedError("Senha atual incorreta.")

        hashed_password = generate_password_hash(new_password)
        return UserRepository.update(user, {"password": hashed_password})

    @staticmethod
    def update_profile(user_id, data):
        user = User.query.get_or_404(user_id)

        # Campos permitidos para o próprio usuário editar
        allowed_fields = ['name', 'phone', 'avatar_url']
        for key in allowed_fields:
            if key in data:
                setattr(user, key, data[key])

        db.session.commit()
        return user

    # --- LÓGICA DE ADMIN ---

    @staticmethod
    def list_all_users_admin():
        return User.query.all()

    @staticmethod
    def update_user_status_admin(user_id, data):
        user = User.query.get_or_404(user_id)

        # Admin pode mudar role e status
        if 'status' in data:
            user.status = data['status']
        if 'role' in data:
            user.role = data['role']

        db.session.commit()
        return user