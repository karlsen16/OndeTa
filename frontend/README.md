# OndeTá? — Frontend

Aplicação React + Vite para o projeto OndeTá?, sistema de localização de pets perdidos

---

## Pré-requisitos

- [Node.js LTS](https://nodejs.org/en/download) instalado 

Após instalar, verifique no terminal:

```bash
node -v
npm -v
```

---

## Configuração pra primeira vez

### 1. Inicializar o projeto com Vite

Dentro da pasta `frontend/`, execute:

```bash
npm create vite@latest . -- --template react
```

Quando perguntar sobre arquivos existentes, escolha **"Ignore files and continue"**.

### 2. Instalar as dependências

```bash
npm install
```

### 3. Instalar o React Router DOM

```bash
npm install react-router-dom
```

---

## Rodar o servidor de desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

---

## Variáveis de ambiente (opcional)

Por padrão, o frontend se conecta ao backend em `http://localhost:5000`.  
Pra usar outra URL, crie um arquivo `.env` na raiz de `frontend/`:

```env
VITE_API_URL=http://localhost:5000
```

---

## Dependências instaladas

| Pacote | Versão | Finalidade |
|---|---|---|
| react | ^19.2.4 | Biblioteca principal |
| react-dom | ^19.2.4 | Renderização no browser |
| react-router-dom | ^7.14.1 | Roteamento entre páginas |
| vite | ^8.0.4 | Bundler e servidor de desenvolvimento |

---

## Observações sobre o backend

O backend Flask precisa estar rodando em `http://localhost:5000` pra que as chamadas de API funcionem  
O CORS já tá configurado no backend pra aceitar as requisições do `localhost:5173`

---

## React + Vite

Esse template tem uma configuração mínima pra usar React com Vite
Atualmente, dois plugins oficiais estão disponíveis:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) usa [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) usa [SWC](https://swc.rs/)




