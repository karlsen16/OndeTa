from app.extensions import db

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)