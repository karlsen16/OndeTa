## 6. Criar diagramas de sequência

### Prioridade

#### Autenticação
- cadastro;
- login;
- desativar conta.

#### Postagens
- criar postagem;
- editar postagem;
- upload/remoção de imagens;
- ocultar postagem.

#### Moderação
- moderar usuário;
- banir usuário;
- moderar postagem.

---

## 7. Criar diagrama de classes

Esse é o melhor momento.

Modelar:
- User;
- Post;
- Image;
- Role;
- Status;
- relações.

### Benefícios
- ajuda MUITO antes da implementação;
- ajuda ORM;
- ajuda schemas;
- ajuda API.

---

## 8. Criar diagramas de atividades

Criar apenas para fluxos importantes:
- login;
- cadastro;
- moderação;
- criação de postagem.

Não precisa exagerar.

---

# FASE 3 — Arquitetura

## Objetivo
Documentar estrutura técnica.

---

## 9. Criar `back_components.puml`

Mostrar:
- controllers;
- services;
- repositories;
- models;
- schemas;
- auth/JWT;
- banco.

---

## 10. Criar `front_components.puml`

Mostrar:
- páginas;
- componentes;
- contextos;
- serviços HTTP;
- gerenciamento de estado.

---

## 11. Criar `ER.puml`

Modelar banco:
- tabelas;
- relacionamentos;
- cardinalidade.

---

## 12. Criar documentos de decisões arquiteturais

Ordem recomendada:

### layered-architecture.md
- por que usar arquitetura em camadas.

### auth-flow.md
- JWT;
- claims;
- autorização.

### moderation-strategy.md
- moderação;
- soft delete;
- ocultação.

### image-storage.md
- upload;
- armazenamento;
- limites.

---

# FASE 4 — API (pré-implementação)

## Objetivo
Planejar contratos antes do código.

---

## 13. Criar `auth.md`

Documentar:
- JWT;
- claims;
- Bearer;
- autorização;
- expiração;
- políticas.

---

## 14. Criar exemplos de requests/responses

Criar:
- auth-examples.md
- post-examples.md
- moderation-examples.md

Contendo:
- requests;
- responses;
- erros.

Isso vai te ajudar MUITO na implementação depois.

---

# FASE 5 — Implementação + Swagger

## Objetivo
Gerar documentação automática.

---

## 15. Implementar schemas Marshmallow

Você já começou isso mentalmente.

---

## 16. Integrar Flask-Smorest

Definir:
- tags;
- responses;
- exemplos;
- auth.

---

## 17. Gerar `openapi.yaml`

Após implementação:
- exportar especificação OpenAPI;
- salvar em `/docs/api/openapi.yaml`.

---

# FASE 6 — Revisão Final

## 18. Revisar consistência

Verificar:
- nomes iguais em todos os diagramas;
- regras coerentes;
- endpoints coerentes;
- schemas coerentes.

---

## 19. Revisar padronização

Padronizar:
- verbos;
- nomes;
- português;
- convenções UML.

---

## 20. Atualizar `README.md`

Adicionar:
- descrição;
- stack;
- arquitetura;
- como executar;
- onde está a documentação.