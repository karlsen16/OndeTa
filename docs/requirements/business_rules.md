# 1. Gestão de Usuários e Autenticação (Auth)

- **[RN01] Identidade Única:** O sistema deve rejeitar qualquer tentativa de cadastro ou atualização que resulte em duplicidade de e-mail.

- **[RN02] Imutabilidade de Papéis (Roles):** O campo `role` não pode ser alterado por usuários comuns. A atribuição do papel `admin` não pode ser realizada através das funcionalidades públicas da aplicação.

- **[RN03] Ciclo de Vida e Acesso:**
    - **Usuários `active`:** Possuem acesso irrestrito às funcionalidades pertinentes ao seu papel.
    - **Usuários `inactive`:** Podem apenas executar o fluxo de reativação da conta.
    - **Usuários `banned`:** Estão impedidos de realizar login ou gerar novos tokens JWT.

- **[RN04] Gerenciamento de Status:** Usuários autenticados com papel `user` podem alterar apenas o próprio status, alternando entre `active` e `inactive`. A atribuição ou remoção do status `banned` é exclusiva de administradores.

- **[RN05] Segurança de Credenciais:** Operações de alteração de senha exigem obrigatoriamente a validação da senha atual antes de persistir a nova.

---

# 2. Regras de Postagens

- **[RN06] Propriedade de Conteúdo (Ownership):** Operações de modificação de postagens são permitidas apenas ao autor da postagem ou a usuários com papel `admin`. Para postagens com status `blocked`, apenas administradores podem realizar modificações.

- **[RN07] Visibilidade Pública:** Somente postagens públicas podem ser retornadas por mecanismos públicos de listagem, busca e visualização coletiva.

- **[RN08] Restrição de Postagens `blocked`:** O autor pode visualizar suas postagens `blocked`, incluindo seus detalhes e localização geográfica, mas não pode editar seus conteúdos, imagens ou alterar seu status.

- **[RN09] Efeito Cascata de Inatividade:** Sempre que um usuário transicionar para `inactive` ou `banned`, o sistema deve automaticamente alterar o status de todas as suas postagens `active` ou `resolved` para `hidden`.

- **[RN10] Integridade Geográfica:** Coordenadas devem ser validadas nos intervalos de latitude `[-90, 90]` e longitude `[-180, 180]`.

---

# 3. Gestão de Imagens e Storage

- **[RN11] Vínculo Obrigatório:** Nenhuma imagem pode existir de forma órfã; o `post_id` deve ser validado e existir antes do processamento do upload.

- **[RN12] Autorização de Upload:** O sistema deve validar se o usuário autenticado é o proprietário da postagem de destino antes de aceitar e processar arquivos de imagem.

- **[RN13] Sincronia de Exclusão:** A exclusão de uma imagem deve garantir a remoção do arquivo armazenado e do respectivo registro persistido, impedindo inconsistências entre armazenamento e banco de dados.

---

# 4. Moderação e Segurança de Dados

- **[RN14] Ofuscação de Recursos Privados:** Postagens que não sejam públicas podem ser acessadas apenas pelo autor da postagem ou por usuários com papel `admin`. Tentativas de acesso por quaisquer outros usuários devem retornar erro `404 Not Found`, simulando a inexistência do recurso.

- **[RN15] Limite de Imagens:** Cada postagem pode possuir no máximo 3 imagens associadas simultaneamente.