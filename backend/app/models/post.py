from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100))
    pet_type = db.Column(db.String(20), nullable=False)                 #cachorro, gato
    category = db.Column(db.String(20), nullable=False)                 #perdido, encontrado
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="active")                 #active, resolved, hidden, blocked
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    images = db.relationship("Image", backref="post", lazy=True, cascade="all, delete-orphan")