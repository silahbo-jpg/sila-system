""
Factory for creating User test instances.

This module provides a UserFactory for generating test User instances with realistic fake data.
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

import factory
from faker import Faker

from tests.factories.base_factory import BaseFactory, CommonFields

fake = Faker()

class UserFactory(BaseFactory):
    """
    Factory for creating User instances for testing.
    
    Generates realistic user data with:
    - Unique emails
    - Realistic names
    - Secure password hashes
    - Various user states (active, inactive, etc.)
    """
    
    class Meta:
        # This should be updated to point to your actual User model
        # Example: from app.models.user import User
        model = "User"  # Replace with actual User model import
        strategy = factory.BUILD_STRATEGY  # Don't persist by default
    
    # Core fields
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    email = factory.LazyFunction(CommonFields.email)
    username = factory.LazyFunction(lambda: f"user_{fake.unique.user_name()}")
    full_name = factory.LazyFunction(lambda: fake.name())
    
    # Authentication
    hashed_password = factory.LazyFunction(
        lambda: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 'secret'
    )
    
    # Status flags
    is_active = True
    is_verified = True
    is_superuser = False
    
    # Timestamps
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyAttribute(lambda o: o.created_at)
    last_login = factory.LazyFunction(
        lambda: fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.utc)
    )
    
    # Profile information
    phone_number = factory.LazyFunction(CommonFields.phone_number)
    date_of_birth = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=18, maximum_age=90)
    )
    
    # Role-based access control
    roles = factory.LazyFunction(lambda: ["user"])
    
    # Class methods for common scenarios
    @classmethod
    def create_superuser(cls, **kwargs) -> 'User':
        """Create a superuser instance."""
        return cls.create(
            is_superuser=True,
            is_verified=True,
            roles=["admin", "user"],
            **kwargs
        )
    
    @classmethod
    def create_inactive(cls, **kwargs) -> 'User':
        """Create an inactive user instance."""
        return cls.create(is_active=False, **kwargs)
    
    @classmethod
    def create_unverified(cls, **kwargs) -> 'User':
        """Create an unverified user instance."""
        return cls.create(is_verified=False, **kwargs)


# Convenience fixtures for tests
def create_user(**kwargs):
    """Create a standard user for testing."""
    return UserFactory.create(**kwargs)


def create_superuser(**kwargs):
    """Create a superuser for testing."""
    return UserFactory.create_superuser(**kwargs)


def create_inactive_user(**kwargs):
    """Create an inactive user for testing."""
    return UserFactory.create_inactive(**kwargs)


def create_unverified_user(**kwargs):
    """Create an unverified user for testing."""
    return UserFactory.create_unverified(**kwargs)
