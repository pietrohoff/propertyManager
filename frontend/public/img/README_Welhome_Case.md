# Welhome — Case (Frontend + API)

> Projeto de exemplo para gerenciar **Imóveis** usando **FastAPI** (backend), **Nginx** servindo front estático (HTML/CSS/JS) e **SQLite** como banco.
>
> Foco em arquitetura simples, fácil de subir com **Docker** e agradável de desenvolver (live reload no front via bind mount).

---

## Sumário
- [Arquitetura](#arquitetura)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Como Rodar (Docker)](#como-rodar-docker)
- [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
- [API (Endpoints)](#api-endpoints)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Decisões de Projeto](#decisões-de-projeto)
- [Troubleshooting](#troubleshooting)
- [Roadmap / Próximos Passos](#roadmap--próximos-passos)
- [Licença](#licença)

---

## Arquitetura

```
[Browser]
   │
   ▼
[Nginx - Frontend]
 - Serve HTML/CSS/JS estático (frontend/public)
 - Proxy de /api/* → backend:8000/api/*
   │
   ▼
[FastAPI - Backend]
 - Rotas REST /api/*
 - SQLModel (ORM) + SQLite
 - Healthcheck /health
   │
   ▼
[SQLite]
 - Arquivo em volume Docker (/data/properties.db)
```

### Por que essa arquitetura?
- **Simplicidade**: Nginx serve o front de forma rápida e faz proxy para a API sem CORS extra.
- **Observabilidade de saúde**: endpoint `/health` e **healthcheck com `curl`** tornam a subida estável.
- **SQLite**: ideal para PoC/dev (zero dependência externa). Em produção, pode ser substituído por Postgres.
- **Gunicorn + Uvicorn**: servidor de produção para apps ASGI (FastAPI). **1 worker** aqui evita corrida no SQLite.

---

## Estrutura de Pastas

```
case/
├── backend/
│   ├── app/
│   │   ├── api/routers/properties.py   # rotas REST de imóveis
│   │   ├── core/config.py              # settings (env)
│   │   ├── db/session.py               # engine, init_db(), get_session()
│   │   ├── main.py                     # FastAPI, /health, include_router
│   │   ├── models/property.py          # modelo SQLModel
│   │   ├── repositories/...            # acesso a dados
│   │   └── schemas/property.py         # pydantic/SQLModel schemas
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── index.html                  # UI (inclui modal de cadastro/edição)
│   │   ├── css/style.css               # estilo responsivo
│   │   └── js/app.js                   # consumo da API e controles do modal
│   ├── nginx.conf                      # proxy /api → backend:8000/api
│   └── Dockerfile
└── docker-compose.yml
```

---

## Como Rodar (Docker)

> Pré-requisitos: **Docker** e **Docker Compose** instalados.

```bash
cd case
docker compose down -v
docker compose build --no-cache
docker compose up
```

- Frontend: **http://localhost:8080**
- API (Swagger): **http://localhost:8000/docs**

### Comandos úteis
- Subir em segundo plano: `docker compose up -d && docker compose logs -f`
- Ver logs: `docker compose logs -f backend` / `docker compose logs -f web`
- Parar e limpar volumes: `docker compose down -v`

---

## Ambiente de Desenvolvimento

Para editar o front e ver alterações **sem rebuild**:
- O `docker-compose.yml` usa **bind mount** da pasta `frontend/public` para `/usr/share/nginx/html`.

Edite os arquivos em `frontend/public/*` e **recarregue o navegador** (Ctrl+F5).

### Desativar cache do HTML (opcional)
No `frontend/nginx.conf`, já há um bloco que pode ser usado para desabilitar cache de `.html`. Ative conforme necessário.

---

## API (Endpoints)

Base: `http://localhost:8000/api`

- `GET /properties` — lista imóveis
- `POST /properties` — cria imóvel
  - body: `{ "title": "...", "address": "...", "status": "active|inactive" }`
- `PUT /properties/{id}` — atualiza imóvel
- `DELETE /properties/{id}` — exclui imóvel

Outros:
- `GET /health` — healthcheck simples (200 OK)

### Modelo `Property`
```json
{
  "id": 1,
  "title": "Apartamento 101",
  "address": "Rua X, 123",
  "status": "active"
}
```

---

## Variáveis de Ambiente

No `docker-compose.yml` (serviço `backend`):

- `DB_PATH` — caminho do arquivo SQLite dentro do container (padrão: `/data/properties.db`)
- `CORS_ORIGINS` — lista de origens permitidas (usado apenas se **não** for servir via Nginx reverse proxy no mesmo host/porta).

> Em dev com Nginx proxy, CORS normalmente **não é necessário** (mesmo domínio/porta do front).

---

## Decisões de Projeto

- **/health** no FastAPI: healthcheck rápido e sem dependência de banco.
- **Healthcheck com `curl`** no Compose: robusto e evita dependências de binários inexistentes.
- **Gunicorn `-w 1`**: com SQLite, múltiplos workers criando tabelas ao mesmo tempo causam corrida. Em bancos externos (Postgres), você pode aumentar a concorrência e usar migrações (Alembic).
- **Bind mount** no front: fluxo de desenvolvimento mais rápido (sem rebuild do container a cada mudança).
- **Nginx**: separa responsabilidades (servir estático + proxy) e melhora compatibilidade de cache/CDN quando necessário.

---

## Troubleshooting

**“container `backend` is unhealthy”**
- Verifique o `/health`: `docker exec -it case-backend-1 curl -f http://127.0.0.1:8000/health`
- Aumente `start_period` no healthcheck se a inicialização do app estiver lenta.
- Confirme que o `DB_PATH` é gravável (`/data` é um volume).

**“table already exists” (SQLite)**
- Certifique-se de estar usando **1 worker** no Gunicorn (já configurado).
- Em prod, use **migrations** e um banco externo (Postgres).

**Mudanças no front não aparecem**
- Com bind mount, recarregue com **Ctrl+F5** (cache do navegador).
- Se não estiver usando bind mount, rode `docker compose build web && docker compose up -d web`.

---

## Roadmap / Próximos Passos

- [ ] Trocar SQLite por Postgres (compose com `postgres` e variável `DATABASE_URL`).
- [ ] Alembic para migrações de schema.
- [ ] Testes (Pytest) e GitHub Actions para CI.
- [ ] Camada de autenticação (JWT) e RBAC básico.
- [ ] Observabilidade: logs estruturados e métricas (/metrics).

---

## Licença

Uso livre para estudo e provas de conceito.
