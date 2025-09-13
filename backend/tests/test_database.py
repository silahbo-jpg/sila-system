"""
Tests for the database functionality.

This module contains tests for SQLAlchemy database operations and utilities.
"""

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db import Base, get_db, async_session_factory, engine
from app.db.models.user import User

# Test model for database operations
class TestModel(Base):
    """Test model for database operations."""
    __tablename__ = "test_model"
    
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.Integer, nullable=True)

@pytest.mark.asyncio
class TestDatabaseOperations:
    """Test cases for database operations."""
    
    async def test_connection(self, db_session: AsyncSession):
        """Test that the database connection is established."""
        # Test SQLAlchemy connection
        result = await db_session.execute(sa.text("SELECT 1"))
        assert result.scalar() == 1
    
    async def test_transaction_commit(self, db_session: AsyncSession):
        """Test transaction commit behavior."""
        test_data = {"name": "test_commit", "value": 42}
        
        # Add a test record
        test_model = TestModel(**test_data)
        db_session.add(test_model)
        await db_session.commit()
        
        # Verify the record was committed
        result = await db_session.execute(
            sa.select(TestModel).where(TestModel.name == "test_commit")
        )
        record = result.scalar_one_or_none()
        assert record is not None
        assert record.value == 42
    
    async def test_transaction_rollback(self, db_session: AsyncSession):
        """Test transaction rollback behavior."""
        test_data = {"name": "test_rollback", "value": 100}
        
        async with db_session.begin():
            test_model = TestModel(**test_data)
            db_session.add(test_model)
            # Intentionally raise an exception to trigger rollback
            raise ValueError("Test rollback")
        
        # Verify the record was not committed
        result = await db_session.execute(
            sa.select(TestModel).where(TestModel.name == "test_rollback")
        )
        record = result.scalar_one_or_none()
        assert record is None
    
    async def test_get_session(self, db_session: AsyncSession):
        """Test getting a database session."""
        assert isinstance(db_session, AsyncSession)
        assert db_session.in_transaction() is False
    
    async def test_get_session_transaction(self, db_session: AsyncSession):
        """Test getting a database session with transaction."""
        async with db_session.begin():
            assert isinstance(db_session, AsyncSession)
            assert db_session.in_transaction() is True


@pytest.mark.asyncio
class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    async def test_user_creation(self, db_session: AsyncSession):
        """Test user creation and retrieval."""
        # Create a test user
        user_data = {
            "email": "test@example.com",
            "hashed_password": "hashed_password",
            "is_active": True,
            "username": "testuser"
        }
        user = User(**user_data)
        db_session.add(user)
        await db_session.commit()
        
        # Verify the user was created
        result = await db_session.execute(
            sa.select(User).where(User.email == "test@example.com")
        )
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.email == "test@example.com"
        assert user.is_active is True


@pytest.fixture
async def test_db():
    """Fixture for database session."""
    async with async_session_factory() as session:
        try:
            # Start a transaction
            await session.begin()
            yield session
        finally:
            # Rollback any changes made during the test
            await session.rollback()
            await session.close()

@pytest.mark.asyncio
class TestDatabaseUtils:
    """Tests for database utility functions."""
    
    async def test_get_db_dependency(self, test_db: AsyncSession):
        """Test the get_db dependency injection."""
        assert isinstance(test_db, AsyncSession)
        
        # Test a simple query
        result = await test_db.execute(sa.text("SELECT 1"))
        assert result.scalar() == 1
