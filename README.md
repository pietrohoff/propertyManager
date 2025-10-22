# Gerenciador de Imóveis

> Projeto de exemplo para gerenciar **Imóveis** usando **FastAPI** (backend), **Nginx** servindo front estático (HTML/CSS/JS) e **SQLite** como banco.
>
> Foco em arquitetura simples, fácil de subir com **Docker** e agradável de desenvolver.

---

## Sumário
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Como Rodar (Docker)](#como-rodar-docker)
- [API (Endpoints)](#api-endpoints)

---

## Estrutura de Pastas

```
propertyManager/
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

```bash
cd propertyManager
docker compose down -v
docker compose build --no-cache
docker compose up
```

- Frontend: **http://localhost:8080**
- API (Swagger): **http://localhost:8000/docs**

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



