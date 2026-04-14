#Usar comando python3 tests.test_db na pasta backend para rodar
from app import create_app
from app.extensions import db
from app.models import User
from app.repositories.pet_repository import PetRepository

app = create_app()


def create_test_user():
    """Cria um usuário de teste se não existir"""
    user = User.query.filter_by(email="teste@email.com").first()

    if not user:
        user = User(
            nome="Usuário Teste",
            email="teste@email.com",
            senha="123"
        )
        db.session.add(user)
        db.session.commit()
        print(f"Usuário criado com ID: {user.id}")
    else:
        print(f"Usuário já existe com ID: {user.id}")

    return user


def create_test_pet(user_id):
    """Cria um pet de teste"""
    pet = PetRepository.create({
        "nome": "Rex",
        "tipo": "cachorro",
        "descricao": "Perdido no centro",
        "status": "perdido",
        "user_id": user_id
    })

    print(f"Pet criado com ID: {pet.id}")
    return pet


def list_pets():
    """Lista todos os pets"""
    pets = PetRepository.get_all()

    print("\nLista de pets:")
    for pet in pets:
        print(f"- {pet.id}: {pet.nome} ({pet.status})")


if __name__ == "__main__":
    with app.app_context():
        print("🔌 Testando conexão com banco...")

        # Criar usuário
        user = create_test_user()

        # Criar pet
        create_test_pet(user.id)

        # Listar pets
        list_pets()

        print("\n✅ Teste finalizado com sucesso!")