from app.extensions import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())