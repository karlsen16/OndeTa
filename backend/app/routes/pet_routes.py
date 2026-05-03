from flask import Blueprint
from app.controllers.pet_controller import PetController
from flask_jwt_extended import jwt_required

pet_bp = Blueprint("pets", __name__, url_prefix="/pets")


@pet_bp.route("", methods=["POST"])
@jwt_required()
def create_pet():
    return PetController.create_pet()


@pet_bp.route("", methods=["GET"])
def get_all_pets():
    return PetController.get_all_pets()


@pet_bp.route("/<int:pet_id>", methods=["GET"])
def get_pet_by_id(pet_id):
    return PetController.get_pet_by_id(pet_id)

@pet_bp.route("/<int:pet_id>", methods=["PUT"])
@jwt_required()
def update_pet(pet_id):
    return PetController.update_pet(pet_id)

@pet_bp.route("/<int:pet_id>", methods=["DELETE"])
@jwt_required()
def delete_pet(pet_id):
    return PetController.delete_pet(pet_id)