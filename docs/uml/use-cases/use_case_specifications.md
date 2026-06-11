# Especificação de Casos de Uso e Regras Globais

## Fluxos Alternativos Globais

Estes fluxos aplicam-se a qualquer caso de uso do sistema, podendo ocorrer em qualquer etapa da execução de uma operação, sem a necessidade de estarem explicitados individualmente em cada especificação.

### FG01. Dados Inválidos (400)

1. Sistema identifica que os dados enviados não seguem o formato esperado. 
2. Sistema rejeita a operação.

### FG02. Parâmetros Inválidos (400)

1. Sistema identifica parâmetros inválidos. 
2. Sistema rejeita a operação.

### FG03. Token Inválido ou Expirado (401)

1. Sistema identifica que o token JWT está ausente, expirado, malformado ou inválido.
2. Sistema interrompe a operação.

### FG04. Conta Sem Permissão de Acesso (403)

1. Sistema identifica que o usuário autenticado não possui permissão para executar a operação solicitada.
2. Sistema interrompe a operação.

### FG05. Erro Interno do Servidor (500)

1. Ocorre uma falha inesperada no servidor ou na comunicação com o banco de dados em qualquer etapa de uma operação.
2. Sistema interrompe a operação.

---

# UC1 — Cadastrar Usuário

| Campo | Descrição                                                                                             |
|---|-------------------------------------------------------------------------------------------------------|
| Objetivo | Permitir que um visitante crie uma nova conta no sistema (RF01).                                      |
| Atores | Visitante                                                                                             |
| Pré-condições | O visitante não deve estar autenticado.                                                               |
| Pós-condições | Usuário registrado no banco de dados com `status: active` e `role: user`, e autenticado na aplicação. |

## Fluxo Principal

1. Ator informa nome, e-mail, senha e, opcionalmente, contato.
2. Sistema valida os dados recebidos.
3. Sistema verifica se o e-mail informado não está em uso.
4. Sistema processa a senha para armazenamento seguro (RNF01).
5. Sistema registra a nova conta no banco de dados. 
6. Sistema gera o token JWT. 
7. Sistema retorna o token JWT e os dados da conta criada, autenticando o usuário automaticamente.

## Fluxos Alternativos

### 3A. E-mail Já Utilizado (409)

1. Sistema identifica que o e-mail já pertence a outra conta (RN01).
2. Sistema rejeita o cadastro.

---

# UC2 — Fazer Login

| Campo | Descrição                                                    |
|---|--------------------------------------------------------------|
| Objetivo | Autenticar um usuário e conceder acesso ao sistema (RF02).   |
| Atores | Visitante                                                    |
| Pré-condições | Possuir conta cadastrada.                                    |
| Pós-condições | Usuário autenticado com status `active` e token JWT emitido. |

## Fluxo Principal

1. Ator informa e-mail e senha.
2. Sistema valida os dados recebidos.
3. Sistema verifica as credenciais.
4. Sistema verifica o status da conta (RN03).
5. Sistema gera um token JWT contendo o identificador e o papel do usuário. 
6. Sistema retorna o token JWT e os dados da conta.

## Fluxos Alternativos

### 3A. Credenciais Inválidas (401)

1. Sistema identifica e-mail inexistente ou senha incorreta.
2. Sistema rejeita a autenticação.

### 4A. Conta com Status `banned` (403)

1. Sistema identifica status `banned`.
2. Sistema rejeita a autenticação.

### 4B. Conta com Status `inactive` (409)

1. Sistema identifica status `inactive`.
2. Sistema rejeita a autenticação e informa que reativação é possível.
   - **[Ponto de Extensão: Solicitação de Reativação]**

---

# UC2.1 — Reativar Conta

| Campo         | Descrição                                                                                |
|---------------|------------------------------------------------------------------------------------------|
| Objetivo      | Reativar uma conta desativada após a rejeição do login padrão (RF05).                    |
| Atores        | Visitante                                                                                |
| Extensões     | Estende **UC2 — Fazer Login** a partir do ponto de extensão `Solicitação de Reativação`. |
| Pré-condições | Conta existente com status `inactive` e credenciais válidas.                             |
| Pós-condições | Conta alterada para status `active`, autenticada e token JWT emitido.                    |

## Condição de Extensão
* Status 409 após tentativa de login.

## Fluxo Principal

1. Sistema oferece a opção de reativação. 
2. Sistema valida os dados recebidos. 
3. Sistema verifica as credenciais. 
4. Sistema verifica o status da conta (RN03, RN04).
5. Sistema altera o status da conta para `active`. 
6. Sistema gera um token JWT contendo o identificador e o papel do usuário. 
7. Sistema retorna o token JWT e os dados da conta.

## Fluxos Alternativos

### 1A. Reativação Cancelada

1. Ator recusa a reativação.
2. Sistema encerra o processo sem autenticar o usuário.

### 3A. Credenciais Inválidas (401)

1. Sistema identifica e-mail inexistente ou senha incorreta.
2. Sistema rejeita a autenticação.

### 4A. Conta com Status `banned` (403)

1. Sistema identifica status `banned`.
2. Sistema rejeita a reativação.

### 4B. Conta com Status `active` (409)

1. Sistema identifica status `active`.
2. Sistema rejeita a reativação.

---

# UC3 — Visualizar Feed

| Campo | Descrição                                                |
|---|----------------------------------------------------------|
| Objetivo | Exibir as postagens públicas em formato de lista (RF11). |
| Atores | Visitante, Usuário, Administrador                        |
| Pré-condições | Nenhuma.                                                 |
| Pós-condições | Feed exibido.                                            |

## Fluxo Principal

1. Ator acessa o feed.
2. Sistema recupera as postagens públicas (RN07).
3. Sistema aplica paginação.
4. Sistema retorna os resultados.
5. Sistema exibe as postagens.
   - **[Ponto de Extensão: Uso de Filtros]**
   - **[Ponto de Extensão: Visualização de Detalhes no Mapa]**

---

# UC3.1 — Filtrar Resultados

| Campo | Descrição                                                                                                     |
|---|---------------------------------------------------------------------------------------------------------------|
| Objetivo | Restringir os resultados exibidos utilizando filtros geográficos e atributos da postagem (RF13).              |
| Atores | Visitante, Usuário, Administrador                                                                             |
| Extensões     | Estende **UC3 — Visualizar Feed** e **UC4 — Visualizar Mapa** a partir do ponto de extensão `Uso de Filtros`. |
| Pré-condições | Existir uma consulta de postagens em andamento.                                                               |
| Pós-condições | Resultados filtrados exibidos.                                                                                |

## Condição de Extensão
* Ator faz utilização de filtros.

## Fluxo Principal

1. Ator informa um ou mais filtros.
2. Sistema valida os parâmetros recebidos.
3. Sistema determina o ponto geográfico de referência.
4. Sistema determina o raio de busca. 
5. Sistema aplica os filtros. 
6. Sistema retorna os resultados. 
7. Sistema exibe as postagens compatíveis.

## Fluxos Alternativos

### 3A. Ponto de Referência Não Informado

1. Ator não informa ponto geográfico.
2. Sistema utiliza a coordenada padrão configurada.
3. Sistema prossegue para o passo 4 do fluxo principal.

### 4A. Raio Não Informado

1. Ator não informa raio.
2. Sistema utiliza o valor padrão de `10 km`.
3. Sistema prossegue para o passo 5 do fluxo principal.

---

# UC3.2 — Exibir Postagem no Mapa

| Campo         | Descrição                                                                                                                                                               |
| ------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Objetivo      | Exibir uma postagem selecionada centralizada no mapa juntamente com seus detalhes (RF14).                                                                               |
| Atores        | Visitante, Usuário, Administrador                                                                                                                                       |
| Extensões     | Estende **UC3 — Visualizar Feed**, **UC4 — Visualizar Mapa** e **UC10 — Visualizar Minhas Postagens** a partir do ponto de extensão `Visualização de Detalhes no Mapa`. |
| Pré-condições | A postagem deve possuir coordenadas geográficas válidas.                                                                                                                |
| Pós-condições | Mapa exibido com a postagem selecionada centralizada e seus detalhes apresentados.                                                                                      |

## Condição de Extensão
* Ator seleciona a opção de visualizar uma postagem no mapa.

## Fluxo Principal

1. Sistema recupera os dados da postagem selecionada. 
2. Sistema abre a visualização do mapa. 
3. Sistema centraliza o mapa nas coordenadas da postagem. 
4. Sistema destaca a postagem selecionada. 
5. Sistema exibe os detalhes da postagem.

## Fluxos Alternativos

### 1A. Postagem Não Encontrada (404)

1. Sistema identifica que a postagem não foi encontrada. 
2. Sistema rejeita a requisição.

### 1B. Postagem Não Pública (404)

1. Sistema identifica que a postagem não é pública. 
2. Sistema rejeita a requisição informando que o recurso não foi encontrado (RN14).

---

# UC4 — Visualizar Mapa

| Campo | Descrição                                                  |
|---|------------------------------------------------------------|
| Objetivo | Exibir as postagens públicas em formato geográfico (RF12). |
| Atores | Visitante, Usuário, Administrador                          |
| Pré-condições | Nenhuma.                                                   |
| Pós-condições | Mapa exibido com os pins correspondentes.                  |

## Fluxo Principal

1. Ator acessa a visualização de mapa. 
2. Sistema recupera as postagens públicas compatíveis com a área consultada (RN07).
3. Sistema verifica se a quantidade de resultados está dentro dos limites permitidos (RNF18).
4. Sistema exibe os pins.
   - **[Ponto de Extensão: Uso de Filtros]**
   - **[Ponto de Extensão: Visualização de Detalhes no Mapa]**

## Fluxos Alternativos

### 3A. Área com Densidade Excessiva (400)

1. Sistema identifica quantidade excessiva de resultados.
2. Sistema interrompe a consulta.

---

# UC5 — Visualizar Meu Perfil

| Campo | Descrição                                               |
|---|---------------------------------------------------------|
| Objetivo | Exibir os dados da conta do usuário autenticado (RF03). |
| Atores | Usuário autenticado.                                    |
| Pré-condições | Nenhuma.                                                |
| Pós-condições | Dados do perfil exibidos.                               |

## Fluxo Principal

1. Ator acessa a área de perfil.
2. Sistema identifica o usuário autenticado.
3. Sistema recupera os dados da conta.
4. Sistema exibe as informações do perfil.

---

# UC6 — Editar Meu Perfil

| Campo | Descrição                                             |
|---|-------------------------------------------------------|
| Objetivo | Atualizar os dados do perfil do usuário autenticado (RF03). |
| Atores | Usuário autenticado.                                  |
| Inclusões | **UC5 — Visualizar Meu Perfil**                       |
| Pré-condições | Usuário autenticado com status `active`.              |
| Pós-condições | Dados do perfil atualizados.                          |

## Fluxo Principal

1. Sistema executa o **UC5 — Visualizar Meu Perfil**.
2. Ator acessa a edição de perfil. 
3. Sistema apresenta os dados atuais. 
4. Ator altera as informações desejadas. 
5. Sistema valida os dados recebidos. 
6. Sistema atualiza o cadastro.
7. Sistema retorna os dados atualizados.

## Fluxos Alternativos

### 5A. E-mail Duplicado (409)

1. Sistema identifica conflito de e-mail (RN01).
2. Sistema impede a alteração.

---

# UC7 — Desativar Minha Conta

| Campo | Descrição                                                 |
|---|-----------------------------------------------------------|
| Objetivo | Permitir que o usuário desative sua própria conta (RF04). |
| Atores | Usuário autenticado.                                      |
| Inclusões | **UC5 — Visualizar Meu Perfil**                           |
| Pré-condições | Usuário autenticado com status `active`.                  |
| Pós-condições | Conta marcada como `inactive`.                            |

## Fluxo Principal

1. Sistema executa o **UC5 — Visualizar Meu Perfil**.
2. Ator solicita a desativação da conta. 
3. Sistema solicita confirmação. 
4. Ator confirma a operação. 
5. Sistema altera o status para `inactive`. 
6. Sistema aplica o efeito cascata de inatividade (RN09). 
7. Sistema encerra a sessão do usuário e redireciona o ator para a tela inicial.

## Fluxos Alternativos

### 4A. Operação Cancelada

1. Ator cancela a confirmação.
2. Sistema encerra o processo.

---

# UC8 — Alterar Minha Senha

| Campo | Descrição |
|---|---|
| Objetivo | Alterar a senha da conta autenticada (RF03). |
| Atores | Usuário autenticado. |
| Inclusões | **UC5 — Visualizar Meu Perfil** |
| Pré-condições | Usuário autenticado com status `active`. |
| Pós-condições | Nova senha registrada. |

## Fluxo Principal

1. Sistema executa o **UC5 — Visualizar Meu Perfil**.
2. Ator informa senha atual. 
3. Ator informa nova senha. 
4. Sistema valida os dados recebidos.
5. Sistema processa a nova senha para armazenamento seguro (RNF01).
6. Sistema atualiza a credencial.

## Fluxos Alternativos

### 4A. Senha Atual Inválida (401)

1. Sistema identifica divergência na senha atual (RN05).
2. Sistema impede a alteração.

---

# UC9 — Fazer uma Postagem

| Campo | Descrição                                                                  |
|---|----------------------------------------------------------------------------|
| Objetivo | Criar uma nova postagem relacionada a um pet perdido ou encontrado (RF06). |
| Atores | Usuário Autenticado                                                        |
| Pré-condições | Usuário autenticado com status `active`.                                   |
| Pós-condições | Postagem criada com status `active`.                                       |

## Fluxo Principal

1. Ator informa as informações do pet e as coordenadas geográficas.
2. Sistema valida os dados recebidos (RN10).
3. Sistema identifica o usuário autenticado. 
4. Sistema cria a postagem. 
5. Sistema associa a postagem ao usuário autenticado. 
6. Sistema retorna os dados da postagem criada.
   - **[Ponto de Extensão: Upload de Imagens]**

---

# UC9.1 — Adicionar Imagens à Postagem

| Campo | Descrição                                                                                                                  |
|---|----------------------------------------------------------------------------------------------------------------------------|
| Objetivo | Associar imagens a uma postagem existente (RF07).                                                                          |
| Atores | Usuário Autenticado                                                                                                        |
| Extensões     | Estende **UC9 — Fazer uma Postagem** e **UC11 — Editar Minha Postagem** a partir do ponto de extensão `Upload de Imagens`. |
| Pré-condições | Usuário autenticado com status `active`.                                                                                   |
| Pós-condições | Imagens vinculadas à postagem.                                                                                             |

## Condição de Extensão
* Ator adiciona imagens à postagem.

## Fluxo Principal

1. Ator envia uma ou mais imagens. 
2. Sistema valida formato (RNF12).
3. Sistema verifica se a postagem não excederá o limite máximo de 3 imagens associadas (RN15).
4. Sistema valida o tamanho dos arquivos (RNF11).
5. Sistema verifica a existência da postagem informada (RN11). 
6. Sistema verifica se o usuário autenticado é proprietário da postagem (RN12). 
7. Sistema verifica se a postagem não possui status `blocked` (RN08). 
8. Sistema realiza o upload (RNF13). 
9. Sistema registra as imagens. 
10. Sistema retorna os dados atualizados.

## Fluxos Alternativos

### 2A. Arquivo Inválido (400)

1. Sistema identifica formato não suportado.
2. Sistema rejeita o upload.

### 3A. Limite de Imagens Excedido (409)

1. A quantidade de imagens ultrapassa o limite permitido.
2. Sistema rejeita a operação.

### 4A. Arquivo Excede o Limite (413)

1. Sistema identifica tamanho superior ao permitido.
2. Sistema rejeita o upload.

### 5A. Postagem Não Encontrada (404)

1. Sistema identifica que a postagem não foi encontrada. 
2. Sistema rejeita a operação.

### 6A. Postagem Não Pertence ao Usuário (403)

1. Sistema identifica ausência de permissão.
2. Sistema rejeita a operação.

### 7A. Postagem `blocked` (403)

1. Sistema identifica status `blocked`.
2. Sistema rejeita a operação.

---

# UC10 — Visualizar Minhas Postagens

| Campo | Descrição                                                |
|---|----------------------------------------------------------|
| Objetivo | Exibir todas as postagens do usuário autenticado (RF10). |
| Atores | Usuário Autenticado                                      |
| Pré-condições | Usuário autenticado com status `active`.                 |
| Pós-condições | Lista de postagens exibida.                              |

## Fluxo Principal

1. Ator acessa seu painel de postagens.
2. Sistema identifica o usuário autenticado.
3. Sistema recupera todas as postagens associadas ao usuário. 
4. Sistema exibe os resultados.
   - **[Ponto de Extensão: Visualização de Detalhes no Mapa]**

---

# UC11 — Editar Minha Postagem

| Campo | Descrição                                           |
|---|-----------------------------------------------------|
| Objetivo | Alterar dados de uma postagem própria (RF08, RF09). |
| Atores | Usuário Autenticado                                 |
| Inclusões | **UC10 — Visualizar Minhas Postagens**              |
| Pré-condições | Usuário autenticado com status `active`.            |
| Pós-condições | Postagem atualizada.                                |

## Fluxo Principal

1. Sistema executa o **UC10 — Visualizar Minhas Postagens**. 
2. Ator altera os dados permitidos de uma postagem (informações do pet, localização ou status permitido). 
3. Sistema valida os dados recebidos (RN10).
4. Sistema verifica a existência da postagem informada. 
5. Sistema verifica se o usuário autenticado é proprietário da postagem (RN06). 
6. Sistema verifica se a postagem não possui status `blocked` (RN08). 
7. Sistema salva as alterações. 
8. Sistema retorna a postagem atualizada.
   - **[Ponto de Extensão: Upload de Imagens]**
   - **[Ponto de Extensão: Remoção de Imagens]**

## Fluxos Alternativos

### 3A. Operação Não Autorizada (403)

1. O status solicitado viola as regras de transição definidas pela RF09.
2. Sistema rejeita a operação.

### 4A. Postagem Não Encontrada (404)

1. Sistema identifica que a postagem não foi encontrada.
2. Sistema rejeita a operação.

### 5A. Postagem Não Pertence ao Usuário (403)

1. Sistema identifica ausência de permissão.
2. Sistema rejeita a operação.

### 6A. Postagem `blocked` (403)

1. Sistema identifica status `blocked` (RN06).
2. Sistema rejeita a atualização.

# UC11.1 — Remover Imagens da Minha Postagem

| Campo | Descrição                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| Objetivo | Remover imagens de uma postagem pertencente ao usuário (RF08).                               |
| Atores | Usuário Autenticado                                                                          |
| Extensões     | Estende **UC11 — Editar Minha Postagem** a partir do ponto de extensão `Remoção de Imagens`. |
| Pré-condições | Usuário autenticado com status `active`.                                                     |
| Pós-condições | Imagem removida da postagem e do armazenamento.                                              |

## Condição de Extensão
* Ator remove imagens da postagem.

## Fluxo Principal

1. Ator seleciona a imagem a ser removida. 
2. Sistema remove o registro da imagem. 
3. Sistema remove o arquivo correspondente do storage (RN13). 
4. Sistema confirma a operação.

## Fluxos Alternativos

### 1A. Imagem Não Encontrada (404)

1. Sistema identifica que a imagem não foi encontrada.
2. Sistema rejeita a operação.

### 1B. Imagem Não Pertence à Postagem (404)

1. Sistema identifica que a imagem informada não está associada à postagem selecionada.
2. Sistema rejeita a operação.

---

# UC12 — Visualizar Usuários

| Campo | Descrição                                                                      |
|---|--------------------------------------------------------------------------------|
| Objetivo | Permitir que administradores consultem usuários cadastrados no sistema (RF15). |
| Atores | Administrador                                                                  |
| Pré-condições | Nenhuma.                                                                       |
| Pós-condições | Lista de usuários retornada.                                                   |

## Fluxo Principal

1. Ator solicita a listagem de usuários cadastrados (enviando ou não parâmetros de busca).
2. Sistema identifica o usuário autenticado.
3. Sistema valida as permissões administrativas (RNF07). 
4. Sistema valida os parâmetros recebidos. 
5. Sistema recupera os usuários cadastrados. 
6. Sistema aplica paginação. 
7. Sistema retorna os resultados.

---

# UC13 — Moderar Usuário

| Campo | Descrição                                           |
|---|-----------------------------------------------------|
| Objetivo | Alterar informações permitidas de qualquer usuário (RF15). |
| Atores | Administrador                                       |
| Pré-condições | Nenhuma.                                            |
| Pós-condições | Dados do usuário atualizados.                       |

## Fluxo Principal

1. Ator solicita a alteração de informações de um usuário.
2. Sistema identifica o usuário autenticado.
3. Sistema valida as permissões administrativas (RNF07). 
4. Sistema valida os dados recebidos.
5. Sistema verifica a existência do cadastro do usuário informado.
6. Sistema verifica se houve solicitação de alteração de status.
   - **[Ponto de Extensão: Restauração / Banimento de Usuário]**
7. Sistema salva as alterações. 
8. Sistema retorna os dados atualizados.

## Fluxos Alternativos

### 4A. E-mail Duplicado (409)

1. Sistema identifica conflito de e-mail (RN01).
2. Sistema impede a alteração.

### 5A. Usuário Não Encontrado (404)

1. Sistema não localiza o usuário solicitado.
2. Sistema encerra a operação.

---

# UC13.1 — Restaurar / Banir Usuário

| Campo | Descrição                                                                                              |
|---|--------------------------------------------------------------------------------------------------------|
| Objetivo | Alterar o status de um usuário para `active` ou `banned` (RF15).                                              |
| Atores | Administrador                                                                                          |
| Extensões     | Estende **UC13 — Moderar Usuário** a partir do ponto de extensão `Restauração / Banimento de Usuário`. |
| Pré-condições | Administrador autenticado e conta a ser alterada existe.                                            |
| Pós-condições | Status do usuário atualizado.                                                                          |

## Condição de Extensão
* Alteração de status de um usuário solicitada por um administrador.

## Fluxo Principal

1. Sistema valida a operação.
2. Caso o novo status seja `banned`:
   - 2.1. Sistema aplica o efeito cascata de inatividade (RN09).
3. Sistema salva as alterações. 
4. Sistema retorna os dados atualizados.

### 1A. Operação Não Autorizada (403)

1. O status solicitado viola as regras de transição definidas pela RF15.
2. Sistema rejeita a operação.

---

# UC14 — Visualizar Postagens

| Campo | Descrição                                                                      |
|---|--------------------------------------------------------------------------------|
| Objetivo | Permitir que administradores consultem postagens existentes no sistema (RF16). |
| Atores | Administrador                                                                  |
| Pré-condições | Nenhuma.                                                                       |
| Pós-condições | Lista de postagens retornada.                                                  |

## Fluxo Principal

1. Ator solicita a listagem de postagens existentes (enviando ou não parâmetros de busca).
2. Sistema identifica o usuário autenticado.
3. Sistema valida as permissões administrativas (RNF07). 
4. Sistema valida os parâmetros recebidos. 
5. Sistema recupera as postagens existentes.
6. Sistema aplica paginação. 
7. Sistema retorna os resultados.

---

# UC15 — Moderar Postagem

| Campo | Descrição                                            |
|---|------------------------------------------------------|
| Objetivo | Alterar informações permitidas de qualquer postagem (RF16). |
| Atores | Administrador                                        |
| Pré-condições | Nenhuma.                                             |
| Pós-condições | Dados da postagem atualizados.                       |

## Fluxo Principal

1. Ator solicita a alteração de informações de uma postagem.
2. Sistema identifica o usuário autenticado.
3. Sistema valida as permissões administrativas (RNF07). 
4. Sistema valida os dados recebidos.
5. Sistema verifica a existência da postagem informada.
6. Sistema verifica se houve solicitação de alteração de status.
7. Sistema salva as alterações. 
8. Sistema retorna os dados atualizados.

## Fluxos Alternativos

### 5A. Postagem Não Encontrada (404)

1. Sistema não localiza a postagem.
2. Sistema encerra a operação.

### 6A. Operação Não Autorizada (403)

1. O status solicitado viola as regras de transição definidas pela RF16.
2. Sistema rejeita a operação.

---

# UC16 — Remover Imagens da Postagem

| Campo | Descrição                                              |
|---|--------------------------------------------------------|
| Objetivo | Remover imagens associadas a qualquer postagem (RF17). |
| Atores | Administrador                                          |
| Pré-condições | Nenhuma.                                               |
| Pós-condições | Imagem removida da postagem e do armazenamento.        |

## Fluxo Principal

1. Ator solicita a remoção de uma imagem.
2. Sistema identifica o usuário autenticado.
3. Sistema valida as permissões administrativas (RNF07). 
4. Sistema valida os dados recebidos.
5. Sistema verifica a existência da imagem. 
6. Sistema remove o registro da imagem. 
7. Sistema remove o arquivo correspondente do storage (RN13). 
8. Sistema confirma a operação.

## Fluxos Alternativos

### 5A. Imagem Não Encontrada (404)

1. Sistema não localiza a imagem.
2. Sistema encerra a operação.