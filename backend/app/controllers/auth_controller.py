from flask import request, jsonify
from app.services.auth_service import AuthService


class AuthController:

    @staticmethod
    def register():
        data = request.get_json()

        try:
            user = AuthService.register(data)

            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def login():
        data = request.get_json()

        try:
            user = AuthService.login(
                data.get("email"),
                data.get("password")
            )

            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 401
