# 1. Estados do Domínio

Esta seção define os estados possíveis das principais entidades do sistema. Esses estados são utilizados pelas regras de negócio, requisitos funcionais e mecanismos de autorização.

## Usuário

| Estado     | Descrição                                                                                    |
| ---------- |----------------------------------------------------------------------------------------------|
| `active`   | Usuário com acesso normal ao sistema e autorizado a autenticar-se.                           |
| `inactive` | Usuário que desativou a própria conta. Não pode utilizar o sistema até realizar a reativação.|
| `banned`   | Usuário bloqueado por um administrador. Não pode autenticar-se nem utilizar o sistema.       |

## Postagem

| Estado     | Descrição                                                          |
| ---------- |--------------------------------------------------------------------|
| `active`   | Caso publicado e ativo.                                            |
| `resolved` | Indica que o caso foi solucionado.                                 |
| `hidden`   | Restrita a proprietários e administradores.                        |
| `blocked`  | Bloqueada por moderação. Não pode ser editada por usuários comuns. |

## Observações

- **Postagens Públicas:** Possuem status `active` ou `resolved`. Elas são as únicas visíveis no feed, mapa e resultados de busca para qualquer tipo de ator (incluindo visitantes).
- **Informações do Pet:** nome do pet, tipo de pet (`cachorro` ou `gato`), categoria (`perdido` ou `encontrado`) e descrição.

# 2. Atores do Sistema

- **Visitante:** Usuário não autenticado.

- **Usuário:** Usuário autenticado (`role: user`).

- **Administrador:** Usuário autenticado com privilégios de moderação (`role: admin`).

---

# 3. Requisitos Funcionais

## 3.1 Gestão de Usuários e Acesso

- **[RF01] Cadastro de Conta:** O sistema deve permitir que visitantes se cadastrem fornecendo nome, e-mail e senha, podendo informar informações de contato opcionalmente.

- **[RF02] Autenticação:** O sistema deve autenticar usuários mediante e-mail e senha válidos.

- **[RF03] Gerenciamento de Perfil:** O usuário deve poder visualizar seu perfil, editar dados (nome, e-mail e informações de contato) e alterar sua senha (mediante validação da senha atual).

- **[RF04] Desativação de Conta:** O usuário deve poder desativar sua própria conta, alterando seu status de `active` para `inactive`.

- **[RF05] Reativação de Conta:** O sistema deve permitir que usuários com status `inactive` solicitem a reativação de sua conta mediante nova validação de credenciais, alterando seu status para `active` e efetuando o login automaticamente. 

---

## 3.2 Funcionalidades de Postagem

- **[RF06] Criação de Postagem:** O usuário deve poder criar postagens enviando obrigatoriamente as informações do pet e uma localização geográfica (`latitude` e `longitude`).

- **[RF07] Upload de Mídia:** O usuário deve poder adicionar imagens às suas postagens, respeitando os formatos e limites definidos pelo sistema.

- **[RF08] Gerenciamento de Postagens:** O usuário deve poder editar os dados de suas próprias postagens (informações do pet e localização) e também adicionar e remover imagens associadas, exceto para postagens com status `blocked`.

- **[RF09] Controle de Status de Postagem:** O usuário deve poder alternar o status de suas postagens entre `active`, `resolved` e `hidden`. O usuário não possui permissão para alterar o status para `blocked`.

- **[RF10] Visualização Pessoal:** O usuário deve poder visualizar em seu painel todas as suas postagens e seus detalhes, incluindo aquelas com status `hidden` e `blocked`.

---

## 3.3 Visualização e Busca

- **[RF11] Feed:** O sistema deve exibir uma lista paginada de postagens públicas.

- **[RF12] Visualização em Mapa:** O sistema deve exibir pins geolocalizados de postagens públicas.

- **[RF13] Busca Geográfica e Filtros:** O sistema deve permitir a busca de postagens públicas utilizando filtros por tipo de pet, categoria e distância máxima em relação a um ponto geográfico de referência informado pelo usuário. Caso nenhum ponto de referência seja informado, deverá ser utilizada uma coordenada padrão configurada pelo sistema. Caso nenhum raio seja informado, deverá ser utilizado um valor padrão de 10 km. Os filtros devem ser aplicáveis tanto no feed quanto no mapa.

- **[RF14] Detalhes da Postagem:** O sistema deve exibir todas as informações e imagens de uma postagem pública selecionada.

---

## 3.4 Moderação (Administrativo)

- **[RF15] Gerenciamento de Usuários:** O administrador deve poder listar todos os usuários, editar informações permitidas de usuários (nome, e-mail e informações de contato) e alterar o status para `active` ou `banned`.

- **[RF16] Moderação de Conteúdos:** O administrador deve poder listar todas as postagens do sistema, editar seus conteúdos (informações do pet e localização) e alterar o status para `hidden` ou `blocked`.

- **[RF17] Remoção de Mídia:** O administrador deve poder deletar permanentemente imagens de qualquer postagem.