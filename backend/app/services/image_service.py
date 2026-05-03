from app.repositories.image_repository import ImageRepository
from app.repositories.pet_repository import PetRepository


class ImageService:

    @staticmethod
    def add_image_to_pet(pet_id, url):
        pet = PetRepository.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet não encontrado")
        if pet.user_id != user_id:
            raise PermissionError("Sem permissão para adicionar imagens")
        return ImageRepository.create({
            "url": url,
            "pet_id": pet_id
        })

    @staticmethod
    def get_images_by_pet(pet_id):
        return ImageRepository.get_by_pet_id(pet_id)

    @staticmethod
    def delete_image(image_id):
        image = ImageRepository.get_by_id(image_id)
        if not image:
            raise ValueError("Imagem não encontrada")
        pet = image.pet
        if pet.user_id != user_id:
            raise PermissionError("Sem permissão para deletar imagem")
        ImageRepository.delete(image)