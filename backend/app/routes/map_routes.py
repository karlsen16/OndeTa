from flask import Blueprint, request
from app.controllers.post_controller import PostController

map_bp = Blueprint("map", __name__, url_prefix="/map")


@map_bp.route("", methods=["GET"])
def get_map_view():
    """
    Retorna a lógica inicial do mapa.
    Se vier ?highlight=ID, o controller pode retornar dados extras
    daquele post específico para o Front já abrir destacado.
    """
    return PostController.get_map_view()

@map_bp.route("/pins", methods=["GET"])
def get_map_pins():
    """
    Retorna uma lista leve de todos os posts ativos.
    Retorno sugerido: [{id, latitude, longitude, category}, ...]
    """
    return PostController.get_map_pins()