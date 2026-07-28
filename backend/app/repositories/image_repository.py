from app.extensions import db
from app.models import Image


class ImageRepository:

    @staticmethod
    def create(data):
        image = Image(**data)
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def get_image(image_id=None, post_id=None):
        query = db.session.query(Image)

        if image_id is not None:
            query = query.filter(Image.id == image_id)
        elif post_id is not None:
            query = query.filter(Image.post_id == post_id)
        else:
            return None

        return query.first()

    @staticmethod
    def get_feed(params):
        query = db.session.query(Image)

        order = params.get("order", None)
        if order == "oldest":
            query = query.order_by(Image.created_at.asc())
        else:
            query = query.order_by(Image.created_at.desc())
        total_images = query.count()

        limit = params.get("limit")
        page = params.get("page")
        offset = (page - 1) * limit
        images = query.offset(offset).limit(limit).all()

        return total_images, images

    @staticmethod
    def delete(image):
        db.session.delete(image)
        db.session.commit()