import uuid
from supabase import create_client
from flask import current_app

def get_supabase():
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_KEY"]
    )

def upload_image(file):
    supabase = get_supabase()

    filename = f"{uuid.uuid4()}.jpg"

    file_bytes = file.read()

    supabase.storage.from_(
        current_app.config["SUPABASE_BUCKET"]
    ).upload(
        path=filename,
        file=file_bytes,
        file_options={
            "content-type": "image/jpeg"
        }
    )

    public_url = supabase.storage.from_(
        current_app.config["SUPABASE_BUCKET"]
    ).get_public_url(filename)

    return {
        "filename": filename,
        "url": public_url
    }


def delete_image_storage(filename):
    supabase = get_supabase()

    supabase.storage.from_(
        current_app.config["SUPABASE_BUCKET"]
    ).remove([filename])