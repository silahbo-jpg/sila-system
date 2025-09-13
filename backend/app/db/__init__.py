"""
Database Package Initialization

This module provides the database connection and session management
for the SILA System using SQLAlchemy with async support.
"""
import os
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from .base import Base
from .models import *  # noqa: F401, F403


def _is_testing_mode() -> bool:
    """
    Detect test mode without depending on .env:
    - PYTEST_CURRENT_TEST present -> True
    - ENVIRONMENT in {"test", "testing"} -> True
    - settings.TESTING (if exists) -> fallback
    """
    if os.getenv("PYTEST_CURRENT_TEST"):
        return True

    env = getattr(settings, "ENVIRONMENT", "").lower()
    if env in {"test", "testing"}:
        return True

    return bool(getattr(settings, "TESTING", False))


def _ensure_asyncpg(url: str) -> str:
    """
    Convert 'postgresql://' to 'postgresql+asyncpg://' for async compatibility.
    Preserves query string (e.g., ?schema=public).
    """
    if not url:
        return url
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


# Detect testing mode
IS_TESTING = _is_testing_mode()

# Choose database URL safely (TEST_DATABASE_URL is optional)
if IS_TESTING and getattr(settings, "TEST_DATABASE_URL", None):
    _raw_url = settings.TEST_DATABASE_URL
else:
    _raw_url = getattr(settings, "ASYNC_DATABASE_URL", None) or getattr(settings, "DATABASE_URL", "")

# Ensure we're using asyncpg
DATABASE_URL = _ensure_asyncpg(_raw_url)

# In tests, use NullPool to avoid persistent connections between test cases
POOL_CLASS = NullPool if IS_TESTING else None

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=getattr(settings, "DEBUG", False),
    future=True,
    pool_pre_ping=True,
    pool_recycle=getattr(settings, "DATABASE_POOL_RECYCLE", 1800),
    pool_size=getattr(settings, "DATABASE_POOL_SIZE", 5),
    max_overflow=getattr(settings, "DATABASE_MAX_OVERFLOW", 10),
    pool_timeout=getattr(settings, "DATABASE_POOL_TIMEOUT", 30),
    poolclass=POOL_CLASS,
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async session.
    
    Yields:
        AsyncSession: An async database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db():
    """
    Get database session (compatibility with FastAPI dependency injection).
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        yield session


__all__ = [
    'engine',
    'AsyncSessionLocal',
    'get_session',
    'get_db',
    'create_tables',
    'drop_tables',
    'Base',
    'models',
    'IS_TESTING',
]
