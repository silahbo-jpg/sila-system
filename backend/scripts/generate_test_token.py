"""
Generate a test JWT token for development and testing.

This script generates a JWT token for a test admin user with admin privileges.
It should only be used in development and testing environments.
"""
import asyncio
import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash

# Load environment variables from .env file
load_dotenv()

# JWT Configuration
JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Database setup
from app.db.session import async_session

async def get_or_create_test_user() -> Dict[str, Any]:
    """Get or create a test admin user with admin privileges."""
    async with async_session() as session:
        try:
            # Check if test user exists
            result = await session.execute(
                select(User).where(User.email == "admin@example.com")
            )
            user = result.scalars().first()

            if not user:
                # Create test admin user
                hashed_password = get_password_hash("admin123")
                user = User(
                    email="admin@example.com",
                    name="Test Admin",
                    hashed_password=hashed_password,
                    role="admin",
                    is_active=True
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                print("✅ Created test admin user")

            return {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "is_active": user.is_active
            }

        except Exception as e:
            await session.rollback()
            print(f"❌ Error getting/creating test user: {e}")
            raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token with the given data and expiration.
    
    Args:
        data: Dictionary containing token claims
        expires_delta: Optional timedelta for token expiration
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": os.urandom(16).hex()
    })
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def main():
    """Generate and print a test JWT token."""
    print("\n=== Generate Test JWT Token ===\n")

    try:
        # Get or create test user
        test_user = await get_or_create_test_user()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Prepare token data with user information
        token_data = {
            "sub": str(test_user["id"]),
            "email": test_user["email"],
            "name": test_user["name"],
            "role": test_user["role"],
            "is_active": test_user["is_active"]
        }

        # Create access token with user ID as subject
        access_token = create_access_token(
            data={"sub": token_data["sub"]},
            expires_delta=access_token_expires
        )

        print(f"🔑 Test Token (expires in {ACCESS_TOKEN_EXPIRE_MINUTES} minutes):")
        print("-" * 50)
        print(access_token)
        print("-" * 50)
        print("\nUser Info:")
        for key, value in token_data.items():
            print(f"{key.capitalize()}: {value}")
        print("\n🔐 Use this token in the Authorization header like this:")
        print(f"Authorization: Bearer {access_token}")

        return 0

    except Exception as e:
        print(f"❌ Error generating test token: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
