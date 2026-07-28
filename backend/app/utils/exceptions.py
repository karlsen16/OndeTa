class APIError(Exception):
    code = 500
    description = "Erro interno no servidor"


    def __init__(self, description=None, code=None, payload=None):
        super().__init__()
        if description:
            self.description = description
        if code:
            self.code = code
        self.payload = payload


    def to_dict(self):
        rv = {
            "status": "error",
            "message": self.description
        }
        if self.payload:
            rv["details"] = self.payload
        return rv


class DensityLimitError(APIError):
    code = 400
    description = "Excedeu o limite ou restrições na requisição"


class UnauthorizedError(APIError):
    code = 401
    description = "Acesso negado. Credenciais inválidas."


class ForbiddenError(APIError):
    code = 403
    description = "Acesso negado. Nível de permissão insuficiente."


class NotFoundError(APIError):
    code = 404
    description = "Recurso não encontrado"


class ConflictError(APIError):
    code = 409
    description = "Requisição infringe restrições"