from pydantic import BaseModel
import os

class Settings(BaseModel):
    db_path: str = os.environ.get("DB_PATH", "/data/properties.db")
    cors_origins: list[str] = [orig.strip() for orig in os.environ.get("CORS_ORIGINS", "").split(",") if orig.strip()]

settings = Settings()
