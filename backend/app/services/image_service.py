from app.extensions import db
from app.models.image import Image
from app.models.post import Post
from app.utils.image_utils import compress_image
from app.services.storage_service import upload_image, delete_image_storage
from werkzeug.exceptions import NotFound, Forbidden


class ImageService:

    @staticmethod
    def create_image(file, post_id, user_id=None, is_admin=False):
        """
        Orquestra: Compressão -> Upload Storage -> Banco de Dados.
        Faz limpeza automática no Storage se o Banco falhar.
        """
        # 1. Validação de posse (se não for admin, checa se o post é do user)
        post = Post.query.get_or_404(post_id)
        if not is_admin and user_id and post.user_id != user_id:
            raise Forbidden("Você não tem permissão para adicionar imagens a este post.")

        # 2. Processamento da imagem (Utils)
        compressed_buffer = compress_image(file)

        # 3. Upload para o Supabase (StorageService)
        # Passamos o buffer para o upload
        storage_data = upload_image(compressed_buffer)
        filename = storage_data["filename"]
        url = storage_data["url"]

        try:
            # 4. Persistência no Banco
            new_image = Image(
                filename=filename,
                url=url,
                post_id=post_id
            )
            db.session.add(new_image)
            db.session.commit()
            return new_image

        except Exception as e:
            db.session.rollback()
            # 5. ROLLBACK MANUAL DO STORAGE: Evita o "Zumbi"
            delete_image_storage(filename)
            raise e

    @staticmethod
    def delete_image(image_id, user_id=None, is_admin=False):
        """
        Deleta a imagem do banco e do storage de forma coordenada.
        """
        image = Image.query.get_or_404(image_id)

        # Validação: Admin pode tudo, User só pode se for dono do post da imagem
        if not is_admin and user_id:
            post = Post.query.get(image.post_id)
            if post.user_id != user_id:
                raise Forbidden("Você não tem permissão para deletar esta imagem.")

        filename = image.filename

        try:
            # Primeiro remove do banco
            db.session.delete(image)
            db.session.commit()

            # Se o banco confirmou, remove do storage
            delete_image_storage(filename)
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_post_images(post_id):
        """Lista imagens de um post específico."""
        return Image.query.filter_by(post_id=post_id).all()