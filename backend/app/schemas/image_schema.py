from marshmallow import Schema, fields, validate


class ImageResponseSchema(Schema):

    id = fields.Int()
    image_url = fields.Url()
    pet_id = fields.Int()


class ImageCreateSchema(Schema):

    image_url = fields.Url(
        required=True,
        validate=validate.Length(max=500)
    )
    pet_id = fields.Int(required=True)