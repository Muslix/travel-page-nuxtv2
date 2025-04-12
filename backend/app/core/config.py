import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Lädt Umgebungsvariablen aus .env-Datei

class Settings(BaseSettings):
    PROJECT_NAME: str = "Schwob aufm Sattl"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "geheimerschluessel123")
    # JWT Token Gültigkeitsdauer in Minuten
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 Tage
    
    # Datenbank
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/schwob_aufm_sattl"
    )
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Frontend lokale Entwicklung
    ]
    
    # Medien
    MEDIA_ROOT: str = "media"
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_HOSTS: list[str] = [
        "localhost",
    ]
    
    class Config:
        case_sensitive = True

settings = Settings()
