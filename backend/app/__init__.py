from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow import ValidationError
from .config import Config
from app.extensions import db, bcrypt, jwt
from app.utils.exceptions import APIError
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    CORS(app, resources={r"/*": {"origins": ["https://karlsen16.github.io", "http://localhost:5173"]}})

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.models import User, Post, Image

    from app.routes.auth_routes import auth_bp
    from app.routes.post_routes import post_bp
    from app.routes.me_routes import me_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.map_routes import map_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(me_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(map_bp)

    return app

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify(error.to_dict()), error.code

    @app.errorhandler(500)
    def handle_unknown_error(error):
        return jsonify({
            "status": "error",
            "message": "Erro inesperado no servidor"
        }), 500

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify({
            "status": "error",
            "message": "Dados inválidos",
            "details": err.messages
        }), 400