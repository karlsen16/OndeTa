from app import create_app
from app.extensions import db
from app.models import User
from app.repositories.post_repository import PostRepository

app = create_app()

def list_posts():
    print("\nLista de pets:")
    repo = PostRepository()
    for i in range(1,11):
        post = repo.get_by_id(i)
        print(f"- {post.id}: {post.pet_name} ({post.status})")


if __name__ == "__main__":
    with app.app_context():
        print("Testando conexão com banco...")
        list_posts()
        print("\n✅ Teste finalizado com sucesso!")