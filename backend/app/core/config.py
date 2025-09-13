# backend/app/core/config.py
import os
import secrets
from typing import List, Optional, Union, Dict, Any
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration.
    Loads from .env file and environment variables.
    """
    
    # =========================
    # Environment
    # =========================
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # =========================
    # Database
    # =========================
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sila_dev"
    TEST_DATABASE_URL: Optional[str] = None
    
    # For backward compatibility
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "sila_dev"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # =========================
    # Security
    # =========================
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # =========================
    # Project
    # =========================
    PROJECT_NAME: str = "SILA System"
    SILA_SYSTEM_ID: str = "sila-dev"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # =========================
    # CORS
    # =========================
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["*"]
    
    # =========================
    # Testing
    # =========================
    TESTING: bool = False
    
    # =========================
    # API Documentation
    # =========================
    OPENAPI_ENABLED: bool = True
    SWAGGER_UI_ENABLED: bool = True
    REDOC_ENABLED: bool = True
    
    # =========================
    # Rate Limiting
    # =========================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "100/minute"
    
    # =========================
    # Metrics and Monitoring
    # =========================
    METRICS_ENABLED: bool = True
    METRICS_PATH: str = "/metrics"
    
    # =========================
    # Logging
    # =========================
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    JSON_LOGS: bool = False
    
    # =========================
    # Database Pool
    # =========================
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800
    
    def __init__(self, **data: Any):
        super().__init__(**data)
        
        # Generate SECRET_KEY if not provided
        if not self.SECRET_KEY:
            self.SECRET_KEY = secrets.token_urlsafe(32)
            
        # Ensure ASYNC_DATABASE_URL is set and uses asyncpg
        if not self.ASYNC_DATABASE_URL:
            self.ASYNC_DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        elif not self.ASYNC_DATABASE_URL.startswith('postgresql+asyncpg://'):
            self.ASYNC_DATABASE_URL = self.ASYNC_DATABASE_URL.replace(
                'postgresql://', 'postgresql+asyncpg://', 1
            )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # =========================
    # First Superuser
    # =========================
    FIRST_SUPERUSER_EMAIL: Optional[str] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None

    # =========================
    # Security Headers
    # =========================
    SECURE_HEADERS: Dict[str, str] = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "same-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    }

    # =========================
    # API Base URL
    # =========================
    API_BASE_URL: str = Field("http://localhost:8000")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost", "http://localhost:8000", "http://127.0.0.1", "http://127.0.0.1:8000"]
    )

    # =========================
    # PostgreSQL Configuration
    # =========================
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "sila_dev"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    # =========================
    # Methods
    # =========================
    def update_database_urls(self) -> None:
        """Always rebuild database URLs based on current PostgreSQL settings."""
        self.DATABASE_URL = (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        self.ASYNC_DATABASE_URL = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Create a single settings instance
settings = Settings()

# =========================
# Singleton Settings
# =========================
@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.update_database_urls()
    return settings
