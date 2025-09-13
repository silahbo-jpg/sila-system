"""
Create an initial admin user.

This script creates an initial admin user with the provided email and password.
"""
import asyncio
import getpass
import logging
import sys
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.core.config import settings
from app.db.base import Base
from app.models.user import User

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database setup
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_valid_email() -> str:
    while True:
        email = input("Enter postgres email: ").strip()
        if "@" in email and "." in email.split("@")[1]:
            return email
        print("Invalid email format. Try again.")

def get_valid_password() -> str:
    while True:
        password = getpass.getpass("Enter admin password (min 8 chars): ")
        if len(password) >= 8:
            confirm = getpass.getpass("Confirm password: ")
            if password == confirm:
                return password
            print("Passwords do not match.")
        else:
            print("Password must be at least 8 characters.")

async def get_db() -> AsyncSession:
    """Get database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_admin_user(email: str, password: str) -> bool:
    """Create or update an admin user"""
    hashed_password = pwd_context.hash(password)
    
    async with async_session() as session:
        try:
            # Check if user exists
            result = await session.execute(
                select(User).where(User.email == email)
            )
            existing_user = result.scalars().first()
            
            if existing_user:
                logger.warning(f"⚠️ User {email} already exists.")
                update_user = input("Update existing user to admin? (y/n): ").lower()
                if update_user == 'y':
                    await session.execute(
                        update(User)
                        .where(User.email == email)
                        .values(
                            role="admin",
                            is_active=True,
                            hashed_password=hashed_password
                        )
                    )
                    await session.commit()
                    logger.info(f"✅ Updated user {email} to admin")
                    return True
                return False
            else:
                # Create new admin user
                admin_user = User(
                    email=email,
                    name="Administrator",
                    hashed_password=hashed_password,
                    role="admin",
                    is_active=True
                )
                session.add(admin_user)
                await session.commit()
                logger.info(f"✅ Created admin user: {email}")
                return True
                
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error creating admin user: {e}")
            return False

async def main():
    print("\n=== Create Admin User ===\n")
    email = get_valid_email()
    password = get_valid_password()
    success = await create_admin_user(email, password)

    if success:
        print("\n✅ Admin user setup completed.")
    else:
        print("\n❌ Admin user setup failed.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
