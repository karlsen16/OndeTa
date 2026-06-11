# quando mudar os models usar:
# alembic revision --autogenerate -m "comment"      /cria migration
# alembic upgrade head                              /envia pro banco de dados

from .user import User
from .post import Post
from .image import Image