from marshmallow import Schema, fields, validate


class UserResponseSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    contact = fields.Str()


class UserUpdateSchema(Schema):

    name = fields.Str(
        required=False,
        validate=validate.Length(min=2, max=100)
    )
    email = fields.Email(required=False)
    password = fields.Str(
        required=False,
        load_only=True,
        validate=validate.Length(min=6)
    )
    contact = fields.Str(required=False)