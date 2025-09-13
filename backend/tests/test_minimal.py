"""
Test case to verify SQLAlchemy database operations in the test environment.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash

@pytest.mark.asyncio
async def test_database_operations():
    """Test SQLAlchemy database operations in test environment."""
    print("\n=== Starting SQLAlchemy database operations test ===")
    
    # Create a new async session
    async with async_session() as session:
        try:
            # Begin a transaction
            await session.begin()
            
            # Test raw SQL query
            print("1. Testing database connection...")
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1
            print("   Database connection successful")
            
            # Test model access
            print("2. Testing model access...")
            print(f"   User model: {User.__name__}")
            
            # Test creating a user
            print("3. Creating test user...")
            test_email = "test_minimal@example.com"
            user = User(
                email=test_email,
                name="Test Minimal",
                hashed_password=get_password_hash("test_password"),
                role="user",
                is_active=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"   Created user with ID: {user.id}")
            
            # Verify user was created
            print("4. Verifying user creation...")
            result = await session.execute(
                select(User).where(User.email == test_email)
            )
            found_user = result.scalars().first()
            assert found_user is not None
            print(f"   Found user: {found_user.id}")
            
            # Clean up
            print("5. Cleaning up...")
            await session.delete(found_user)
            await session.commit()
            print("   Test user deleted")
            
        except Exception as e:
            await session.rollback()
            print(f"\n[ERROR] Test failed:")
            print(f"- Error type: {type(e).__name__}")
            print(f"- Error message: {str(e)}")
            raise
            
        finally:
            # Ensure the session is closed
            await session.close()
            print("6. Database session closed")