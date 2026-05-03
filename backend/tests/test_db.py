from app import create_app
from app.extensions import db
from app.models import User
from app.repositories.pet_repository import PetRepository

app = create_app()

def list_pets():
    pets = PetRepository.get_all()

    print("\nLista de pets:")
    for pet in pets:
        print(f"- {pet.id}: {pet.name} ({pet.status})")


if __name__ == "__main__":
    with app.app_context():
        print("Testando conexão com banco...")
        list_pets()
        print("\n✅ Teste finalizado com sucesso!")