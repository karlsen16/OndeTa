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
                "nome": pet.nome,
                "status": pet.status
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_all_pets():
        pets = PetService.get_all_pets()

        result = []
        for pet in pets:
            result.append({
                "id": pet.id,
                "nome": pet.nome,
                "status": pet.status
            })

        return jsonify(result), 200

    @staticmethod
    def get_pet_by_id(pet_id):
        try:
            pet = PetService.get_pet_by_id(pet_id)

            return jsonify({
                "id": pet.id,
                "nome": pet.nome,
                "descricao": pet.descricao,
                "status": pet.status
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 404