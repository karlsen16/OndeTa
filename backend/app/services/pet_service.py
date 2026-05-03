from datetime import datetime
from app.repositories.pet_repository import PetRepository
from app.repositories.user_repository import UserRepository


class PetService:

    @staticmethod
    def create_pet(data):
        user = UserRepository.get_by_id(data.get("user_id"))
        if not user:
            raise ValueError("Usuário não encontrado")
        pet_data = {
            "name": data.get("name"),
            "type": data.get("type"),
            "description": data.get("description"),
            "status": data.get("status", "perdido"),
            "date": datetime.utcnow(),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "user_id": user.id
        }
        pet = PetRepository.create(pet_data)
        return pet

    @staticmethod
    def get_all_pets():
        return PetRepository.get_all()

    @staticmethod
    def get_pet_by_id(pet_id):
        pet = PetRepository.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet não encontrado")
        return pet

    @staticmethod
    def update_pet(pet_id, user_id, data):
        pet = PetRepository.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet não encontrado")
        if pet.user_id != user_id:
            raise PermissionError(
                "Sem permissão para editar este pet"
            )
        updated_pet = PetRepository.update(pet, data)
        return updated_pet

    @staticmethod
    def delete_pet(pet_id, user_id):
        pet = PetRepository.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet não encontrado")
        if pet.user_id != user_id:
            raise PermissionError(
                "Sem permissão para deletar este pet"
            )
        PetRepository.delete(pet)