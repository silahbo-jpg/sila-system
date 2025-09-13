# scripts/recreate-critical-files.py
import os
from pathlib import Path

PROJECT_sila_dev-system = Path(__file__).parent.parent

# Definição dos arquivos críticos e seus conteúdos padrão
CRITICAL_FILES = {
    "backend/app/main.py": """
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine, get_db
from app.routers import api_router
from app.middleware.audit_middleware import AuditMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up resources
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware personalizado
app.add_middleware(AuditMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}

@app.get("/")
async def sila_dev-system():
    return {"message": "Bem-vindo ao Sistema sila_dev"}
""",
    
    "backend/app/db/database.py": """
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
import logging

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    poolclass=NullPool if settings.TESTING else None,
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()
""",
    
    "backend/app/core/config.py": """
import os
import secrets
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias
    PROJECT_NAME: str = "Sistema sila_dev"
    PROJECT_DESCRIPTION: str = "Sistema Integrado de Licenciamento e Atendimento"
    VERSION: str = "0.1.0"
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
    ]

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:Truman1*@localhost:5432/sila_dev")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "False").lower() in ("true", "1", "t")
    TESTING: bool = os.getenv("TESTING", "False").lower() in ("true", "1", "t")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
""",
}

def recreate_file(relative_path, content):
    file_path = PROJECT_sila_dev-system / relative_path
    
    # Cria diretórios se não existirem
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Verifica se o arquivo existe e está corrompido
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                current_content = f.read()
                
            # Verifica se o conteúdo contém "otif" (possível corrupção)
            if "otif" in current_content:
                print(f"⚠️ Arquivo {relative_path} parece estar corrompido. Recriando...")
                file_path.write_text(content, encoding="utf-8")
                print(f"✅ Arquivo {relative_path} recriado com sucesso.")
            else:
                print(f"✓ Arquivo {relative_path} parece estar íntegro.")
        else:
            print(f"⚠️ Arquivo {relative_path} não encontrado. Criando...")
            file_path.write_text(content, encoding="utf-8")
            print(f"✅ Arquivo {relative_path} criado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao processar {relative_path}: {e}")
        print(f"⚠️ Recriando {relative_path}...")
        file_path.write_text(content, encoding="utf-8")
        print(f"✅ Arquivo {relative_path} recriado com sucesso.")

if __name__ == "__main__":
    print("🔄 Verificando e recriando arquivos críticos se necessário...")
    
    for path, content in CRITICAL_FILES.items():
        recreate_file(path, content)
    
    print("\n✨ Verificação de arquivos críticos concluída.")

