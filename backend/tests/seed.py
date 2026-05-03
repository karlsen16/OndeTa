import requests
import random

BASE_URL = "http://127.0.0.1:5000"

# =========================================================
# USUÁRIOS
# senha = ID + zeros até completar 6 dígitos
# Ex:
# 1 -> 100000
# 2 -> 200000
# 14 -> 140000
# =========================================================

users = [
    {"name": "Silvia", "email": "silvia@email.com"},
    {"name": "Lucas", "email": "lucas@email.com"},
    {"name": "Paulo", "email": "paulo@email.com"},
    {"name": "Sandra", "email": "sandra@email.com"},
    {"name": "Magali", "email": "magali@email.com"},
    {"name": "Maria", "email": "maria@email.com"},
    {"name": "José", "email": "jose@email.com"},
    {"name": "Francisca", "email": "francisca@email.com"},
    {"name": "Joana", "email": "joana@email.com"},
    {"name": "Cintia", "email": "cintia@email.com"},
]

# =========================================================
# PETS
# =========================================================

pets = [
    {
        "name": "Luna",
        "type": "gato",
        "description": "Gata branca com olhos azuis, porte pequeno, muito dócil.",
        "status": "perdido",
        "user_id": 1
    },
    {
        "name": "Max",
        "type": "cachorro",
        "description": "Labrador amarelo, porte grande, usa coleira vermelha.",
        "status": "perdido",
        "user_id": 2
    },
    {
        "name": "Mimi",
        "type": "gato",
        "description": "Gata cinza listrada, porte pequeno, muito assustada.",
        "status": "perdido",
        "user_id": 3
    },
    {
        "name": "Rex",
        "type": "cachorro",
        "description": "Pastor alemão, porte grande, pelagem preta e marrom.",
        "status": "perdido",
        "user_id": 4
    },
    {
        "name": "Felix",
        "type": "gato",
        "description": "Gato laranja, porte médio, orelhinha cortada.",
        "status": "encontrado",
        "user_id": 5
    },
    {
        "name": "Bella",
        "type": "cachorro",
        "description": "Poodle branca, porte pequeno.",
        "status": "perdido",
        "user_id": 6
    },
    {
        "name": "Nina",
        "type": "gato",
        "description": "Gata persa branca, olhos verdes.",
        "status": "encontrado",
        "user_id": 7
    },
    {
        "name": "Charlie",
        "type": "cachorro",
        "description": "Beagle tricolor, porte médio.",
        "status": "perdido",
        "user_id": 8
    },
    {
        "name": "Thor",
        "type": "gato",
        "description": "Gato siamês de olhos azuis.",
        "status": "perdido",
        "user_id": 9
    },
    {
        "name": "Rocky",
        "type": "cachorro",
        "description": "Bulldog inglês malhado.",
        "status": "perdido",
        "user_id": 10
    },
]

# =========================================================
# COORDENADAS ALEATÓRIAS EM CURITIBA
# =========================================================

def random_curitiba_coordinates():
    lat = round(random.uniform(-25.60, -25.35), 6)
    lon = round(random.uniform(-49.38, -49.18), 6)
    return lat, lon


# =========================================================
# SENHA
# =========================================================

def generate_password(user_id):
    return str(user_id) + ("0" * (6 - len(str(user_id))))


# =========================================================
# LOGIN
# =========================================================

def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    if response.status_code != 200:
        print(f" Erro login: {email}")
        print(response.text)
        return None

    return response.json()["access_token"]


# =========================================================
# CRIAR USUÁRIOS
# =========================================================

def create_users():
    print("\n Criando usuários...")

    created_users = []

    for index, user in enumerate(users, start=1):

        password = generate_password(index)

        contact = f"4199{random.randint(1000000, 9999999)}"

        payload = {
            "name": user["name"],
            "email": user["email"],
            "password": password,
            "contact": contact
        }

        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=payload
        )

        if response.status_code != 201:
            print(f" Erro criando usuário: {user['name']}")
            print(response.text)
            continue

        print(f" Usuário criado: {user['name']} | senha: {password}")

        created_users.append({
            "id": index,
            "email": user["email"],
            "password": password
        })

    return created_users


# =========================================================
# CRIAR PETS
# =========================================================

def create_pets(created_users):
    print("\n Criando pets...")

    tokens = {}

    # login de todos usuários
    for user in created_users:

        token = login(
            user["email"],
            user["password"]
        )

        tokens[user["id"]] = token

    # cria pets
    for pet in pets:

        lat, lon = random_curitiba_coordinates()

        payload = {
            "name": pet["name"],
            "type": pet["type"],
            "description": pet["description"],
            "status": pet["status"],
            "latitude": lat,
            "longitude": lon
        }

        token = tokens.get(pet["user_id"])

        response = requests.post(
            f"{BASE_URL}/pets",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code != 201:
            print(f" Erro criando pet: {pet['name']}")
            print(response.text)
            continue

        print(f" Pet criado: {pet['name']}")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("\n SEED DO BANCO\n")
    created_users = create_users()
    create_pets(created_users)

    print("\n Processo finalizado com sucesso!")