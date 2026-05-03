from marshmallow import Schema, fields, validate
from app.schemas.user_schema import UserResponseSchema


class LoginSchema(Schema):

    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )
    contact = fields.Str(required=False)


class AuthResponseSchema(Schema):

    access_token = fields.Str()
    user = fields.Nested(UserResponseSchema)
