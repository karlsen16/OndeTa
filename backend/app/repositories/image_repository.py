from app.extensions import db
from app.models import Image


class ImageRepository:

    @staticmethod
    def create(image_data):
        image = Image(**image_data)
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def get_by_id(image_id):
        return db.session.get(Image, image_id)

    @staticmethod
    def get_by_pet_id(pet_id):
        return Image.query.filter_by(pet_id=pet_id).all()

    @staticmethod
    def delete(image):
        db.session.delete(image)
        db.session.commit()