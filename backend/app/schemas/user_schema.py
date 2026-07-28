from marshmallow import Schema, fields, validate


class UserResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    contact = fields.Str()


class ProfileResponseSchema(UserResponseSchema):
    posts = fields.Nested("PostResponseSchema", many=True, dump_only=True)


class AdminResponseSchema(UserResponseSchema):
    status = fields.Str()
    role = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    posts = fields.Nested("PostResponseSchema", many=True, dump_only=True)


class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    contact = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["active", "inactive", "banned"]))


class PasswordUpdateSchema(Schema):
    old_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    new_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))


class AdminPaginationSchema(Schema):
    page = fields.Int(validate=validate.Range(min=1), load_default=1)
    limit = fields.Int(validate=validate.Range(min=1, max=100), load_default=20)