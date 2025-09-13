import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import async_session

@pytest.fixture
def db_session():
    """Fixture that provides a database session for testing."""
    return async_session()

@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    """Test that we can connect to the database and execute a simple query."""
    async with db_session as session:
        # Execute a simple query to test the connection
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        
        # Verify we got the expected result
        assert value == 1

