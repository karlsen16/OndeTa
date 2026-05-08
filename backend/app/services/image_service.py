from app.repositories.image_repository import ImageRepository


class ImageService:

    @staticmethod
    def create_image(data):
        return ImageRepository.create(data)


    @staticmethod
    def get_images_by_pet(pet_id):
        return ImageRepository.get_by_pet_id(pet_id)


    @staticmethod
    def get_by_id(image_id):
        return ImageRepository.get_by_id(image_id)


    @staticmethod
    def delete_image(image_id):
        image = ImageRepository.get_by_id(image_id)

        if not image:
            return False

        ImageRepository.delete(image)

        return True