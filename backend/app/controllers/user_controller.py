from flask import jsonify
from app.repositories.user_repository import UserRepository


class UserController:

    @staticmethod
    def get_all_users():
        users = UserRepository.get_all()

        result = []
        for user in users:
            result.append({
                "id": user.id,
                "nome": user.nome,
                "email": user.email
            })

        return jsonify(result), 200

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        return jsonify({
            "id": user.id,
            "nome": user.nome,
            "email": user.email
        }), 200