from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.session import init_db
from .core.config import settings
from .api.routers import properties

app = FastAPI(title="Welhome API (FastAPI)")

# CORS (only if needed; when using Nginx reverse proxy on /api same-origin, not needed)
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
def on_startup():
    init_db()


@app.get('/health')
def health():
    return {'status': 'ok'}

app.include_router(properties.router, prefix="/api")
