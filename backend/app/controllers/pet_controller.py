from flask import request, jsonify
from app.services.pet_service import PetService


class PetController:

    @staticmethod
    def create_pet():
        data = request.get_json()

        try:
            pet = PetService.create_pet(data)

            return jsonify({
                "id": pet.id,
                "name": pet.name,
                "status": pet.status
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_all_pets():
        user_id = request.args.get("user_id", type=int)

        if user_id:
            pets = PetService.get_pets_by_user(user_id)
        else:
            pets = PetService.get_all_pets()

        result = []
        for pet in pets:
            result.append({
                "id": pet.id,
                "name": pet.name,
                "type": pet.type,
                "description": pet.description,
                "status": pet.status,
                "date": pet.date.isoformat() if pet.date else None,
                "latitude": pet.latitude,
                "longitude": pet.longitude,
                "user_id": pet.user_id,
            })

        return jsonify(result), 200

    @staticmethod
    def get_pet_by_id(pet_id):
        try:
            pet = PetService.get_pet_by_id(pet_id)

            return jsonify({
                "id": pet.id,
                "name": pet.name,
                "type": pet.type,
                "description": pet.description,
                "status": pet.status,
                "date": pet.date.isoformat() if pet.date else None,
                "latitude": pet.latitude,
                "longitude": pet.longitude,
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def delete_pet(pet_id):
        data = request.get_json() or {}
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400

        try:
            PetService.delete_pet(pet_id, user_id)
            return jsonify({}), 204

        except PermissionError as e:
            return jsonify({"error": str(e)}), 403

        except ValueError as e:
            return jsonify({"error": str(e)}), 404