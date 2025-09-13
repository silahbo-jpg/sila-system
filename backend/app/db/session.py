# backend/app/db/session.py
"""
Database session management using SQLAlchemy.

This module provides database session management using SQLAlchemy's async session
with lazy initialization to avoid circular imports.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Lazy initialization variables
_engine: Optional[AsyncEngine] = None
_async_session_factory = None
Base = declarative_base()

# =========================
# Lazy Initialization
# =========================
def get_engine() -> AsyncEngine:
    """Get or create the database engine with lazy initialization."""
    global _engine
    if _engine is None:
        from app.core.config import settings  # Import here to avoid circular imports
        
        _engine = create_async_engine(
            settings.ASYNC_DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            future=True,
            pool_pre_ping=True,
            pool_recycle=settings.DATABASE_POOL_RECYCLE,
            poolclass=NullPool if getattr(settings, 'ENVIRONMENT', 'development') == "testing" else None,
        )
    return _engine

def get_async_session_factory():
    """Get or create the async session factory with lazy initialization."""
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
    return _async_session_factory

# For backward compatibility
engine = property(get_engine)
async_session_factory = property(get_async_session_factory)

# =========================
# Dependency
# =========================
async def get_db() -> AsyncSession:
    """
    FastAPI dependency to provide a database session.
    Ensures commit/rollback/close lifecycle is handled safely.
    """
    session_factory = get_async_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# =========================
# DB Initialization
# =========================
async def init_db():
    """
    Initialize database tables (only used for local dev / testing).
    """
    async with get_engine().begin() as conn:
        # Import models here so they are registered with SQLAlchemy Base
        from app.db import models
        await conn.run_sync(Base.metadata.create_all)

# For backward compatibility
SessionLocal = property(get_async_session_factory)
