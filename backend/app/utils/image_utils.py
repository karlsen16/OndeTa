from PIL import Image
from io import BytesIO

MAX_SIZE = (1200, 1200)

def compress_image(file):
    image = Image.open(file)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.thumbnail(MAX_SIZE)

    output = BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=75,
        optimize=True
    )

    output.seek(0)

    return output