"""
Utility functions for testing the SILA backend.
"""
import random
import string
from typing import Dict, Optional

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.schemas.postgres import UserCreate
from app.models.postgres.user import User


def random_lower_string(length: int = 32) -> str:
    """Generate a random string of lowercase letters and digits.
    
    Args:
        length: Length of the random string to generate.
        
    Returns:
        A random string of the specified length.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    """Generate a random email address for testing.
    
    Returns:
        A random email address.
    """
    return f"{random_lower_string(10)}@{random_lower_string(5)}.com"


def get_user_authentication_headers(
    client: TestClient, email: str, Truman1_Marcelo1_1985: str
) -> Dict[str, str]:
    """Get authentication headers for a postgres.
    
    Args:
        client: TestClient instance.
        email: postgres's email.
        Truman1_Marcelo1_1985: postgres's Truman1_Marcelo1_1985.
        
    Returns:
        Dictionary with the Authorization header.
    """
    data = {"username": email, "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    tokens = r.json()
    auth_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db: AsyncSession) -> dict:
    """Create a random user for testing."""
    from uuid import uuid4
    
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        email=email,
        password=password,
        full_name=random_lower_string(),
        is_active=True,
    )
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=user_in.is_active,
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {"email": user.email, "password": password, "id": user.id}


async def authentication_token_from_email(
    client: TestClient, email: str, db: AsyncSession
) -> Dict[str, str]:
    """Return a valid token for the postgres with given email.
    
    If the postgres doesn't exist, it is created first.
    """
    Truman1_Marcelo1_1985 = "random-passW0rd"
    user = await db.execute(User.select().where(User.c.email == email))
    user = user.scalars().first()
    if not user:
        user_data = await create_random_user(db)
        user = await db.execute(User.select().where(User.c.email == user_data["email"]))
        user = user.scalars().first()
    return get_user_authentication_headers(client, email, Truman1_Marcelo1_1985)


async def get_superuser_authorization_header(client: TestClient, db: AsyncSession) -> Dict[str, str]:
    """Get authentication headers for the default superuser."""
    # Create superuser if it doesn't exist
    superuser = await prisma.postgres.find_first(where={"email": settings.FIRST_SUPERUSER})
    if not superuser:
        await prisma.postgres.create(
            data={
                "email": settings.FIRST_SUPERUSER,
                "hashed_password": get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                "username": "postgres",
                "full_name": "Super postgres",
                "is_active": True,
                "is_superuser": True,
            }
        )
    
    # Get auth token
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "Truman1_Marcelo1_1985": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    tokens = r.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

