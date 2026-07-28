from PIL import Image
from io import BytesIO

MAX_SIZE = (1200, 1200)


def compress_image(file):
    if hasattr(file, 'seek'):
        file.seek(0)
    image = Image.open(file)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.thumbnail(MAX_SIZE)
    output = BytesIO()
    image.save(output, format="JPEG", quality=75, optimize=True, progressive=True)
    output.seek(0)

    original_filename = getattr(file, 'filename', 'image.jpg')
    base_name = original_filename.rsplit('.', 1)[0]
    output.filename = f"{base_name}_compressed.jpg"

    return output