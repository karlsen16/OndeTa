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

class InputError(APIError):
    code = 400
    description = "Dados de entrada inválidos"

class UnauthorizedError(APIError):
    code = 401
    description = "Credenciais inválidas ou acesso não autorizado"

class ForbiddenError(APIError):
    code = 403
    description = "Você não tem permissão para realizar esta ação"

class ResourceNotFoundError(APIError):
    code = 404
    description = "Recurso não encontrado"

class ConflictError(APIError):
    code = 409
    description = "Este email já está sendo utilizado"

class OversizedContentError(APIError):
    code = 413
    description = "Excedeu o limite ou restrições na requisição"