from flask import Blueprint
from app.controllers.pet_controller import PetController

pet_bp = Blueprint("pets", __name__, url_prefix="/pets")


@pet_bp.route("", methods=["POST"])
def create_pet():
    return PetController.create_pet()


@pet_bp.route("", methods=["GET"])
def get_all_pets():
    return PetController.get_all_pets()


@pet_bp.route("/<int:pet_id>", methods=["GET"])
def get_pet_by_id(pet_id):
    return PetController.get_pet_by_id(pet_id)