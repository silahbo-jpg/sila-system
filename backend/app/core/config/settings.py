# backend/app/core/config/settings.py
import secrets
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global project settings.
    Valores são carregados do arquivo .env ou variáveis de ambiente.
    """

    # =========================
    # Test Mode
    # =========================
    testing: bool = False

    # =========================
    # Required Settings
    # =========================
    ASYNC_DATABASE_URL: str = ""  # Será ajustado no __init__
    TEST_DATABASE_URL: str = ""
    SECRET_KEY: str = secrets.token_hex(32)  # ⚠️ Substituir em produção!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    PROJECT_NAME: str = "SILA System"
    SILA_SYSTEM_ID: str = "postgres-dev"
    VERSION: str = "0.1.0"

    # =========================
    # PostgreSQL Configuration
    # =========================
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Truman1_Marcelo1_1985"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str | None = None

    @property
    def database_url(self) -> str:
        """
        Retorna a URL do banco de dados.
        Usa a definida em .env ou constrói dinamicamente.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL.split("?")[0]  # Remove parâmetros extras
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # =========================
    # API Configuration
    # =========================
    API_V1_STR: str = "/api/v1"

    # =========================
    # API Docs
    # =========================
    OPENAPI_ENABLED: bool = True
    SWAGGER_UI_ENABLED: bool = True
    REDOC_ENABLED: bool = True

    # =========================
    # CORS
    # =========================
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # =========================
    # Superuser inicial
    # =========================
    FIRST_SUPERUSER: str | None = None
    FIRST_SUPERUSER_PASSWORD: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
        # Ajusta ASYNC_DATABASE_URL dinamicamente, se não for definido
        if not self.ASYNC_DATABASE_URL:
            self.ASYNC_DATABASE_URL = self.database_url.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    """
    Retorna a instância única de Settings (cacheada).
    """
    return Settings()


# Instância global para uso em toda a aplicação
settings = get_settings()
