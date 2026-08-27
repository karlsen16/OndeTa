from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from app.services.user_service import UserService
from app.controllers.auth_controller import AuthController
from app.schemas.user_schema import (
    UserResponseSchema,
    UserUpdateSchema,
    PasswordUpdateSchema
)

user_response_schema = UserResponseSchema()
users_response_schema = UserResponseSchema(many=True)
user_update_schema = UserUpdateSchema()
password_update_schema = PasswordUpdateSchema()


class UserController:

    @staticmethod
    def get_current_user():
        user = AuthController.authenticate_and_authorize()
        return jsonify(user_response_schema.dump(user)), 200

    @staticmethod
    def update_password():
        user = AuthController.authenticate_and_authorize()
        data = password_update_schema.load(request.get_json())
        UserService.update_password(user, data.get("old_password"), data.get("new_password"))
        return jsonify({}), 204

    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()

        return jsonify(users_response_schema.dump(users)), 200

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = UserService.get_user_by_id(user_id)

            return jsonify(user_response_schema.dump(user)), 200

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 404

    @staticmethod
    def update_user(user_id):
        try:
            current_user_id = int(get_jwt_identity())
            if current_user_id != user_id:
                return jsonify({"error": "Sem permissão para editar este usuário"}), 403
            data = user_update_schema.load(request.get_json())
            user = UserService.update_user(user_id, data)

            return jsonify(user_response_schema.dump(user)), 200

        except ValidationError as err:
            return jsonify(
                err.messages
            ), 400

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 404

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500