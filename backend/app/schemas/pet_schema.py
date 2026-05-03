from marshmallow import Schema, fields, validate

PET_TYPES = ["cachorro", "gato"]
PET_TYPE_ERROR_MSG = "O tipo do pet deve ser 'cachorro' ou 'gato'."
PET_STATUS = ["perdido", "encontrado"]
PET_STATUS_ERROR_MSG = "O status deve ser 'perdido' ou 'encontrado'."


class PetResponseSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    description = fields.Str()
    status = fields.Str()
    date = fields.DateTime()
    latitude = fields.Float()
    longitude = fields.Float()
    user_id = fields.Int()


class PetCreateSchema(Schema):

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    type = fields.Str(
        required=True,
        validate=validate.OneOf(
            PET_TYPES,
            error=PET_TYPE_ERROR_MSG
        )
    )
    description = fields.Str(required=False)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(
            PET_STATUS,
            error=PET_STATUS_ERROR_MSG
        )
    )
    date = fields.DateTime(required=False)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


class PetUpdateSchema(Schema):

    name = fields.Str(
        required=False,
        validate=validate.Length(min=2, max=100)
    )
    type = fields.Str(
        required=False,
        validate=validate.OneOf(
            PET_TYPES,
            error=PET_TYPE_ERROR_MSG
        )
    )
    description = fields.Str(required=False)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            PET_STATUS,
            error=PET_STATUS_ERROR_MSG
        )
    )
    date = fields.DateTime(required=False)
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)