from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from app.services.auth_service import AuthService
from app.schemas.auth_schema import (
    LoginSchema,
    RegisterSchema,
    AuthResponseSchema
)
from app.schemas.user_schema import UserResponseSchema

login_schema = LoginSchema()
register_schema = RegisterSchema()
user_response_schema = UserResponseSchema()
auth_response_schema = AuthResponseSchema()


class AuthController:

    @staticmethod
    def register():

        try:
            data = register_schema.load(request.get_json())
            user = AuthService.register(data)

            return jsonify(user_response_schema.dump(user)), 201

        except ValidationError as err:
            return jsonify(err.messages), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def login():
        try:
            data = login_schema.load(request.get_json())
            user = AuthService.login(
                data.get("email"),
                data.get("password")
            )
            access_token = create_access_token(identity=str(user.id))
            response = {
                "access_token": access_token,
                "user": user_response_schema.dump(user)
            }
            return jsonify(auth_response_schema.dump(response)), 200

        except ValidationError as err:
            return jsonify(err.messages), 400

        except ValueError as e:
            return jsonify({"error": str(e)}), 401