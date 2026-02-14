"""Configuration management using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import List
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    # App Configuration
    APP_NAME: str = "Task Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/taskmanager_db"
    
    # JWT Configuration
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
