from marshmallow import Schema, fields, validate


class ImageResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Url()
    post_id = fields.Int()


class ImageCreateSchema(Schema):
    url = fields.Url(required=True, validate=validate.Length(max=500))
    post_id = fields.Int(required=True)