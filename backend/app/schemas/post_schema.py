from marshmallow import Schema, fields, validate

PET_TYPES = ["cachorro", "gato"]
CATEGORIES = ["perdido", "encontrado"]


class PostCreateSchema(Schema):
    pet_name = fields.Str(allow_none=True, validate=validate.Length(max=100))
    pet_type = fields.Str(required=True, validate=validate.OneOf(PET_TYPES))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    description = fields.Str(allow_none=True)
    date = fields.DateTime()
    latitude = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=True, validate=validate.Range(min=-180, max=180))


class PinsRequestSchema(Schema):
    pet_type = fields.Str(validate=validate.OneOf(PET_TYPES))
    category = fields.Str(validate=validate.OneOf(CATEGORIES))
    status = fields.Str(validate=validate.OneOf(["active", "resolved"]))
    latitude = fields.Float(validate=validate.Range(min=-90, max=90), load_default=-25.4311)
    longitude = fields.Float(validate=validate.Range(min=-180, max=180), load_default=-49.2718)
    distance = fields.Float(validate=validate.Range(min=1, max=50), load_default=10)
    limit = fields.Int(validate=validate.Range(min=1), load_default=200)


class FeedRequestSchema(PinsRequestSchema):
    page = fields.Int(validate=validate.Range(min=1), load_default=1)
    limit = fields.Int(validate=validate.Range(min=1, max=100), load_default=20)


class PostUpdateSchema(Schema):
    pet_name = fields.Str(allow_none=True, validate=validate.Length(max=100))
    pet_type = fields.Str(validate=validate.OneOf(PET_TYPES))
    category = fields.Str(validate=validate.OneOf(CATEGORIES))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["active", "resolved", "hidden", "blocked"]))
    date = fields.DateTime()
    latitude = fields.Float(validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=validate.Range(min=-180, max=180))


class PinResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    pet_type = fields.Str()
    category = fields.Str()
    status = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()


class PostResponseSchema(PinResponseSchema):
    pet_name = fields.Str()
    description = fields.Str()
    date = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested("UserResponseSchema", only=("id", "name", "email", "contact"), dump_only=True)
    images = fields.Nested("ImageResponseSchema", many=True, dump_only=True)