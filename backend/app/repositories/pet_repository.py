from app.extensions import db
from app.models import Pet


class PetRepository:

    @staticmethod
    def create(pet_data):
        pet = Pet(**pet_data)
        db.session.add(pet)
        db.session.commit()
        return pet

    @staticmethod
    def get_all():
        return Pet.query.all()

    @staticmethod
    def get_by_user_id(user_id):
        return Pet.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(pet_id):
        return Pet.query.get(pet_id)

    @staticmethod
    def delete(pet):
        db.session.delete(pet)
        db.session.commit()