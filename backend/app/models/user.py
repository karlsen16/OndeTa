from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20))
    status = db.Column(db.String(20), default="active")             #active, inactive, banned
    role = db.Column(db.String(20), default="user")                 #user, admin

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete-orphan")