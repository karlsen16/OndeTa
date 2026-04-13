# Estrutura geral do projeto

```bash
ondeTa/
├── frontend/
├── backend/
├── docs/      
└── README.md
```

## Front-end (React)

```bash
frontend/
├── public/
├── src/
│   ├── assets/          # imagens, ícones
│   ├── components/      # componentes reutilizáveis
│   │   ├── Navbar/
│   │   ├── PetCard/     # exemplo de componente
│   │   │   ├── index.jsx
│   │   │   ├── styles.css
│   │   │   └── iPetCard.test.js (opcional)
│   │   ├── MapView/
│   │   └── ImageUpload/
│   │
│   ├── pages/           # páginas da aplicação
│   │   ├── Login/
│   │   ├── Register/
│   │   ├── Feed/
│   │   ├── CreatePost/
│   │   └── Profile/
│   │
│   ├── hooks/           # lógica reutilizável
│   │   ├── useAuth.js
│   │   ├── usePets.js
│   │   └── useMap.js
│   │
│   ├── context/         # estado global
│   │   └── AuthContext.jsx
│   │
│   ├── services/        # comunicação com API
│   │   └── api.js
│   │
│   ├── utils/           # helpers
│   │   ├── formatDate.js
│   │   └── geoUtils.js
│   │
│   ├── routes/          # configuração de rotas
│   │   └── AppRoutes.jsx
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── vite.config.js (ou webpack)
```

### Organização lógica
- pages → telas completas
- components → peças reutilizáveis
- hooks → lógica separada (muito importante!)
- services → API (axios/fetch)
- context → estado global (auth)

## Back-end (Flask)

```bash
backend/
├── app/
│   ├── __init__.py
│   │
│   ├── routes/              # endpoints
│   │   ├── auth_routes.py
│   │   ├── pet_routes.py
│   │   └── user_routes.py
│   │
│   ├── controllers/         # interface HTTP
│   │   ├── auth_controller.py
│   │   ├── pet_controller.py
│   │   └── user_controller.py
│   │
│   ├── services/            # regras de negócio
│   │   ├── auth_service.py
│   │   ├── pet_service.py
│   │   └── image_service.py
│   │
│   ├── repositories/        # acesso ao banco
│   │   ├── user_repository.py
│   │   ├── pet_repository.py
│   │   └── image_repository.py
│   │
│   ├── models/              # ORM (SQLAlchemy)
│   │   ├── user.py
│   │   ├── pet.py
│   │   └── image.py
│   │
│   ├── schemas/             # validação (marshmallow/pydantic)
│   │   ├── user_schema.py
│   │   └── pet_schema.py
│   │
│   ├── utils/
│   │   ├── security.py      # hash, JWT
│   │   └── helpers.py
│   │
│   ├── config.py
│   └── extensions.py        # db, jwt, etc
│
├── migrations/              # alembic
├── tests/
├── run.py
├── requirements.txt
└── .env
```

### Como isso se conecta (fluxo real)

Frontend → routes → controllers → services → repositories → DB

### Exemplo real (criar pet)

```bash
pet_routes.py        → define endpoint
pet_controller.py    → valida request
pet_service.py       → regra de negócio
pet_repository.py    → salva no banco
```

## Pasta de documentação

```bash
docs/
├── docs/
│   ├── arquitetura.puml
│   ├── componentes_front.puml
│   ├── componentes_back.puml
│   └── sequencia.puml
│
└── README.md
```