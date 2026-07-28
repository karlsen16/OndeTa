from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.exceptions import UnauthorizedError
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginSchema, RegisterSchema, AuthResponseSchema

register_schema = RegisterSchema()
login_schema = LoginSchema()
auth_response = AuthResponseSchema()


class AuthController:
    @staticmethod
    def _handle_auth_response(token, user, status_code=200):
        response_data = {
            "access_token": token,
            "user": user
        }
        return jsonify(auth_response.dump(response_data)), status_code


    @staticmethod
    def authenticate_and_authorize (admin_required=False, include_assets=False, lean=False):
        try:
            verify_jwt_in_request()
        except Exception:
            raise UnauthorizedError("Token inválido, expirado ou ausente.")

        claims = get_jwt()
        if claims.get("ip") != request.remote_addr:
            raise UnauthorizedError("Acesso negado. Origem da requisição inválida.")

        context = {
            "user_id": claims.get("sub"),
            "user_role": claims.get("role"),
            "admin_required": admin_required,
            "include_assets": include_assets,
            "lean": lean
        }

        return AuthService.get_aa_user(**context)


    @staticmethod
    def register():
        data = register_schema.load(request.get_json())
        token, user = AuthService.register(data, ip_address=request.remote_addr)
        return AuthController._handle_auth_response(token, user, 201)


    @staticmethod
    def login(reactivation=False):
        data = login_schema.load(request.get_json())
        token, user = AuthService.login(data, ip_address=request.remote_addr, reactivation=reactivation)
        return AuthController._handle_auth_response(token, user, 200)