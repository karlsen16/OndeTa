from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    from app.models import User, Pet, Image

    from app.routes.auth_routes import auth_bp
    from app.routes.pet_routes import pet_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pet_bp)
    app.register_blueprint(user_bp)

    return app