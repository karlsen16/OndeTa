from app.extensions import db

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "filename": self.filename,
            "pet_id": self.pet_id
        }