# Arquitetura

```mermaid
flowchart LR
    User[Usuário] --> FE[Front-end React]

    FE -->|HTTP/JSON| BE[Back-end Flask API]

    BE --> DB[(Banco de Dados)]
    BE --> IMG[Serviço de Imagens]
    FE --> MAP[API de Mapas]

    IMG -->|URL| BE
    
```

# Front-end
 
## Auth
- login(email, senha)
- register(dados)
- logout()
- getCurrentUser()
- JWT?
- contexto global (AuthContext)?

## Feed
- fetchPets(filtros)
- paginatePets(page)
- filterByLocation(lat, lng, radius)

## Postagem
- createPetPost(data)
- uploadImage(file)
- validateForm()

## Mapa
- loadMap()
- addMarkers(pets)
- getUserLocation()

## Perfil
- getUserPosts(userId)
- editUser()

```mermaid
flowchart TD
    App --> AuthContext
    App --> Pages

    Pages --> Login
    Pages --> Cadastro
    Pages --> Feed
    Pages --> CriarPost
    Pages --> Perfil

    Feed --> PetCard
    CriarPost --> UploadImage
    Feed --> MapView

    App --> API[api.js]
    
```

# Back-end

## Camadas bem definidas
Routes → Controllers → Services → Repositories → Database

```mermaid
flowchart TD
    Routes --> Controllers
    Controllers --> Services
    Services --> Models
    Models --> DB[(Banco de Dados)]

    Services --> External[Serviços Externos]
    
```
## Componentes
### Routes
Define endpoints, exemplo:

```python
@app.route("/pets", methods=["POST"])
def create_pet():
```

### Controllers
Responsável por:

- validar entrada
- chamar service
- retornar resposta

Exemplo:
```python
def create_pet_controller():
    data = request.json
    validate(data)
    pet = pet_service.create_pet(data)
    return jsonify(pet)
```
### Services (regra de negócio)
- create_pet(data)
- find_pets(filters)
- update_pet_status(id)
- associate_image(pet_id, url)

### Repositories (acesso ao banco)
- save_pet(pet)
- get_pet_by_id(id)
- list_pets()

### Auth Service
- generate_token(user)
- verify_token(token)
- hash_password()

### Integrações externas
- upload imagem
- mapas

# ER

```mermaid
erDiagram
    USER {
        int id
        string nome
        string email
        string senha
        string telefone
    }

    PET {
        int id
        string nome
        string tipo
        string descricao
        string status
        date data
        float latitude
        float longitude
        int user_id
    }

    IMAGE {
        int id
        string url
        int pet_id
    }

    USER ||--o{ PET : possui
    PET ||--o{ IMAGE : tem
    
```


# de Sequência (Criar Post)

```mermaid
sequenceDiagram
    participant U as Usuário
    participant FE as Front-end
    participant BE as Back-end
    participant DB as Banco de Dados
    participant IMG as Serviço de Imagem

    U->>FE: Preenche formulário
    FE->>BE: POST /pets

    BE->>DB: Salva dados do pet
    DB-->>BE: OK

    FE->>IMG: Upload da imagem
    IMG-->>FE: URL da imagem

    FE->>BE: POST /upload (URL)
    BE->>DB: Salva URL

    BE-->>FE: Sucesso
    FE-->>U: Post criado
    
```
