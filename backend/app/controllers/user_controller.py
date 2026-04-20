from flask import request, jsonify
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class UserController:

    @staticmethod
    def get_all_users():
        users = UserRepository.get_all()

        result = []
        for user in users:
            result.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "contact": user.contact
            })

        return jsonify(result), 200

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "contact": user.contact
        }), 200

    @staticmethod
    def update_password(user_id):
        data = request.get_json() or {}
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return jsonify({"error": "current_password e new_password são obrigatórios"}), 400

        try:
            UserService.update_password(user_id, current_password, new_password)
            return jsonify({}), 204

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete_user(user_id):
        try:
            UserService.delete_account(user_id)
            return jsonify({}), 204

        except ValueError as e:
            return jsonify({"error": str(e)}), 404
