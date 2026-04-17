# PetService
# valida user
# cria pet
# cria imagens

from datetime import datetime
from app.repositories.pet_repository import PetRepository
from app.repositories.user_repository import UserRepository
from app.repositories.image_repository import ImageRepository


class PetService:

    @staticmethod
    def create_pet(data):
        user = UserRepository.get_by_id(data.get("user_id"))
        if not user:
            raise ValueError("Usuário não encontrado")

        pet_data = {
            "nome": data.get("nome"),
            "tipo": data.get("tipo"),
            "descricao": data.get("descricao"),
            "status": data.get("status", "perdido"),
            "data": datetime.utcnow(),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "user_id": user.id
        }

        pet = PetRepository.create(pet_data)

        images = data.get("images", [])
        for url in images:
            ImageRepository.create({
                "url": url,
                "pet_id": pet.id
            })

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