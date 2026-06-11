from marshmallow import Schema, fields, validate
from app.schemas.user_schema import UserResponseSchema
from app.schemas.image_schema import ImageResponseSchema

PET_TYPES = ["cachorro", "gato"]
CATEGORIES = ["perdido", "encontrado"]

class PostResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    pet_name = fields.Str()
    pet_type = fields.Str()
    category = fields.Str()
    description = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    date = fields.DateTime()
    latitude = fields.Float()
    longitude = fields.Float()

    author = fields.Nested(UserResponseSchema, only=("id", "name", "email", "contact"), dump_only=True)
    images = fields.Nested(ImageResponseSchema, many=True, dump_only=True)


class PinResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    latitude = fields.Float(dump_only=True)
    longitude = fields.Float(dump_only=True)
    pet_type = fields.Str(dump_only=True)
    category = fields.Str(dump_only=True)


class PostCreateSchema(Schema):
    pet_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    pet_type = fields.Str(required=True, validate=validate.OneOf(PET_TYPES))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    description = fields.Str()
    date = fields.DateTime()
    latitude = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=True, validate=validate.Range(min=-180, max=180))


class MapPinsRequestSchema(Schema):
    pet_type = fields.Str(validate=validate.OneOf(PET_TYPES))
    category = fields.Str(validate=validate.OneOf(CATEGORIES))
    latitude = fields.Float(validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=validate.Range(min=-180, max=180))


class PostUpdateSchema(MapPinsRequestSchema):
    pet_name = fields.Str(validate=validate.Length(min=2, max=100))
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(["active", "resolved", "hidden", "blocked"]))


class FeedRequestSchema(MapPinsRequestSchema):
    status = fields.Str(validate=validate.OneOf(["active", "resolved"]))
    page = fields.Int(validate=validate.Range(min=1))
    limit = fields.Int(validate=validate.Range(min=1, max=100))
    distance = fields.Int(validate=validate.Range(min=1, max=50))