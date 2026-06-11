from marshmallow import Schema, fields, validate


class UserResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    contact = fields.Str()
    status = fields.Str()


class AdminResponseSchema(UserResponseSchema):
    role = fields.Str()


class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    contact = fields.Str()
    status = fields.Str(validate=validate.OneOf(["active", "inactive", "banned"]))


class UpdatePasswordSchema(Schema):
    old_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    new_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))


class AdminPaginationSchema(Schema):
    page = fields.Int(validate=validate.Range(min=1), load_default=1)
    limit = fields.Int(validate=validate.Range(min=1, max=100), load_default=20)