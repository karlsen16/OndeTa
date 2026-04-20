from app.extensions import db

class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(20))
    date = db.Column(db.DateTime)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    images = db.relationship("Image", backref="pet", lazy=True)