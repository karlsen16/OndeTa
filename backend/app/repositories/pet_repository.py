from app.extensions import db
from app.models import Pet


class PetRepository:

    @staticmethod
    def create(data):
        pet = Pet(**data)
        db.session.add(pet)
        db.session.commit()
        return pet

    @staticmethod
    def get_all():
        return Pet.query.all()

    @staticmethod
    def get_by_id(pet_id):
        return Pet.query.get(pet_id)

    @staticmethod
    def update(pet, data):
        for key, value in data.items():
            setattr(pet, key, value)
        db.session.commit()
        return pet

    @staticmethod
    def delete(pet):
        db.session.delete(pet)
        db.session.commit()