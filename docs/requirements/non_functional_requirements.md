# 1. Segurança

- **[RNF01] Criptografia de Senhas:** As senhas devem ser processadas com o algoritmo `bcrypt` antes da persistência.

- **[RNF02] Comunicação Criptografada:** O tráfego de dados deve ocorrer obrigatoriamente via HTTPS (`SSL/TLS`).

- **[RNF03] Prevenção de Injeção SQL:** O sistema deve utilizar mecanismos que previnam ataques de injeção SQL em todas as operações de acesso ao banco de dados.

- **[RNF04] Sanitização de Conteúdo:** O sistema deve neutralizar conteúdo potencialmente executável fornecido pelos usuários antes da exibição.

---

# 2. Autenticação e Autorização

- **[RNF05] Autenticação Stateless:** O sistema deve utilizar tokens JWT para autenticação stateless dos usuários.

- **[RNF06] Expiração de Acesso:** Os tokens JWT devem expirar em `24 horas`.

- **[RNF07] Controle de Acesso (RBAC):** O sistema deve verificar privilégios (`role`) para acesso às funcionalidades administrativas.

---

# 3. Desempenho e Escalabilidade

- **[RNF08] Resposta Rápida:** O sistema deve responder consultas de leitura autenticadas ou públicas em até 500 ms para 95% das requisições em condições normais de operação.

- **[RNF09] Eficiência de Busca Geográfica:** O sistema deve utilizar índices espaciais para otimizar consultas geográficas.

- **[RNF10] Eficiência de Tráfego:** Paginação obrigatória com limite padrão de `20 registros`.

---

# 4. Limites de Upload e Armazenamento

- **[RNF11] Limite de Mídia:** Upload máximo de `5MB` por imagem.

- **[RNF12] Formatos Permitidos:** Suporte exclusivo para `JPG`, `JPEG` e `PNG`.

- **[RNF13] Armazenamento de Arquivos:** Os arquivos de mídia devem ser armazenados separadamente do banco de dados relacional.

---

# 5. Usabilidade

- **[RNF14] Simplicidade de Fluxo:** A criação de postagem deve ser concluída em no máximo 3 etapas principais.

- **[RNF15] Feedback de Interface:** Notificações visuais para erros de validação e confirmação de ações.

---

# 6. Responsividade

- **[RNF16] Design Multitela:** A interface deve adaptar-se a dispositivos móveis, tablets e computadores.

---

# 7. Disponibilidade e Confiabilidade

- **[RNF17] Uptime do Serviço:** O sistema deve operar de acordo com a disponibilidade garantida pela infraestrutura utilizada.

- **[RNF18] Controle de Volume Geográfico:** O sistema deve limitar a quantidade de registros geográficos retornados por consulta para preservar o desempenho de renderização do cliente.