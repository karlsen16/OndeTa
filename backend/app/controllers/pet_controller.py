from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from app.services.pet_service import PetService
from app.schemas.pet_schema import (
    PetCreateSchema,
    PetUpdateSchema,
    PetResponseSchema
)

pet_create_schema = PetCreateSchema()
pet_update_schema = PetUpdateSchema()
pet_response_schema = PetResponseSchema()
pets_response_schema = PetResponseSchema(many=True)


class PetController:

    @staticmethod
    def create_pet():
        try:
            data = pet_create_schema.load(request.get_json())
            user_id = int(get_jwt_identity())
            data["user_id"] = user_id
            pet = PetService.create_pet(data)

            return jsonify(pet_response_schema.dump(pet)), 201

        except ValidationError as err:
            return jsonify(err.messages), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_all_pets():
        pets = PetService.get_all_pets()

        return jsonify(pets_response_schema.dump(pets)), 200

    @staticmethod
    def get_pet_by_id(pet_id):
        try:
            pet = PetService.get_pet_by_id(pet_id)

            return jsonify(pet_response_schema.dump(pet)), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def update_pet(pet_id):
        try:
            data = pet_update_schema.load(request.get_json())
            user_id = int(get_jwt_identity())
            pet = PetService.update_pet(
                pet_id,
                user_id,
                data
            )
            return jsonify(pet_response_schema.dump(pet)), 200

        except ValidationError as err:
            return jsonify(err.messages), 400

        except PermissionError as e:
            return jsonify({
                "error": str(e)
            }), 403

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 404

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def delete_pet(pet_id):
        try:
            user_id = int(get_jwt_identity())
            PetService.delete_pet(
                pet_id,
                user_id
            )

            return jsonify({
                "message": "Pet deletado com sucesso"
            }), 200

        except PermissionError as e:
            return jsonify({
                "error": str(e)
            }), 403

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 404

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500