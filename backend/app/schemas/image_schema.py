from marshmallow import Schema, fields, ValidationError, validate

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_file_extension(file_obj):
    if not file_obj or not file_obj.filename:
        raise ValidationError("Arquivo inválido ou sem nome.")

    ext = file_obj.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Extensão de arquivo não permitida. Extensões aceitas: {', '.join(ALLOWED_EXTENSIONS)}")


def validate_file_size(file_obj):
    file_obj.seek(0, 2)
    size = file_obj.tell()
    file_obj.seek(0)

    if size > MAX_FILE_SIZE:
        raise ValidationError(f"O arquivo é muito grande. O tamanho máximo permitido é de {MAX_FILE_SIZE // (1024 * 1024)}MB.")


class ImageResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Url()
    filename = fields.Str()
    post_id = fields.Int()


class ImageUploadSchema(Schema):
    file = fields.Raw(required=True, validate=[validate_file_extension, validate_file_size])