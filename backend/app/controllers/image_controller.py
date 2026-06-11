from flask import request, jsonify
from app.services.image_service import ImageService
from app.services.pet_service import PetService
from app.schemas.image_schema import ImageResponseSchema
from flask_jwt_extended import get_jwt_identity
from app.utils.storage import upload_image, delete_image_storage
from app.utils.image_utils import compress_image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024

image_schema = ImageResponseSchema()
images_schema = ImageResponseSchema(many=True)

def allowed_file(filename):
    return (
        filename and
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


class ImageController:

    @staticmethod
    def create_image(pet_id):

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

        file = request.files.get("image")

        if not file:
            return jsonify({
                "error": "Imagem não enviada"
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "error": "Formato inválido"
            }), 400

        file.seek(0, 2)
        size = file.tell()
        file.seek(0)

        if size > MAX_FILE_SIZE:
            return jsonify({
                "error": "Imagem muito grande"
            }), 400

        compressed = compress_image(file)
        uploaded = upload_image(compressed)

        image = ImageService.create_image({
            "url": uploaded["url"],
            "filename": uploaded["filename"],
            "pet_id": pet_id
        })

        return jsonify(image_schema.dump(image)), 201



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