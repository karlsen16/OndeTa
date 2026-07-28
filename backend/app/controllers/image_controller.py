from flask import request, jsonify
from app.services.image_service import ImageService
from app.services.post_service import PostService
from app.schemas.image_schema import ImageResponseSchema, ImageUploadSchema
from flask_jwt_extended import get_jwt_identity
from app.services.storage_service import upload_image, delete_image_storage
from app.utils.image_utils import compress_image

image_schema = ImageResponseSchema()
images_schema = ImageResponseSchema(many=True)


class ImageController:

    @staticmethod
    def create_image(post_id):

        user_id = int(get_jwt_identity())
        pet = PetService.get_pet_by_id(pet_id)

        if not pet:
            return jsonify({
                "error": "Pet não encontrado"
            }), 404

        if pet.user_id != user_id:
            return jsonify({
                "error": "Sem permissão"
            }), 403


        validated = ImageUploadSchema().load(request.files)
        uploaded = upload_image(compress_image(validated['file']))

        new_image = ImageService.save_image({
            "url": uploaded["url"],
            "filename": uploaded["filename"],
            "post_id": post_id
        })

        return jsonify(ImageResponseSchema().dump(new_image)), 201


    @staticmethod
    def get_pet_images(pet_id):

        pet = PetService.get_pet_by_id(pet_id)

        if not pet:
            return jsonify({
                "error": "Pet não encontrado"
            }), 404

        images = ImageService.get_images_by_pet(pet_id)

        return jsonify(images_schema.dump(images)), 200

    @staticmethod
    def delete_image(pet_id, image_id):

        user_id = int(get_jwt_identity())
        pet = PetService.get_pet_by_id(pet_id)

        if not pet:
            return jsonify({
                "error": "Pet não encontrado"
            }), 404

        if pet.user_id != user_id:
            return jsonify({
                "error": "Sem permissão"
            }), 403

        image = ImageService.get_by_id(image_id)

        if not image:
            return jsonify({
                "error": "Imagem não encontrada"
            }), 404

        if image.pet_id != pet_id:
            return jsonify({
                "error": "Imagem não pertence ao pet"
            }), 400

        delete_image_storage(image.filename)
        ImageService.delete_image(image_id)

        return jsonify({
            "message": "Imagem removida"
        }), 200