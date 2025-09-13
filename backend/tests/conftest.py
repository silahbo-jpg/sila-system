"""
Pytest configuration and fixtures for integration tests.
"""
import os
import sys
import logging
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Import and configure test logging first to ensure it's set up before any other imports
from tests.logging_config import configure_test_logging

# Apply test logging configuration
configure_test_logging()

# Now import application code
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from fastapi.testclient import TestClient

# Use a separate test database
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:Truman1_Marcelo1_1985@localhost:5432/sila_test"

@pytest.fixture(scope="session")
async def engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
        future=True,
        poolclass=NullPool
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(engine):
    """Create a test database session."""
    connection = await engine.connect()
    transaction = await connection.begin()
    session_maker = sessionmaker(
        bind=connection,
        expire_on_commit=False,
        class_=AsyncSession
    )
    session = session_maker()
    
    # Override the get_db dependency
    async def override_get_db():
        try:
            yield session
        finally:
            await session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client
    
    # Clear overrides after test
    app.dependency_overrides.clear()
