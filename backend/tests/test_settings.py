"""
Test settings for the SILA System backend.

This module provides test-specific settings that override the default settings
for testing purposes.
"""
import os

# Set up test environment variables before importing the main settings
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/sila_test"
os.environ["ASYNC_DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:5432/sila_test"
os.environ["PRISMA_DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/sila_test"
os.environ["DATABASE_POOL_SIZE"] = "5"
os.environ["DATABASE_MAX_OVERFLOW"] = "10"
os.environ["DATABASE_POOL_TIMEOUT"] = "30"
os.environ["DATABASE_POOL_RECYCLE"] = "1800"
os.environ["DATABASE_ECHO"] = "False"
os.environ["TESTING"] = "True"  # ✅ garante que o campo testing: bool é carregado corretamente

# Now import the main settings
from app.core.config import Settings  # noqa: E402


class TestSettings(Settings):
    """Test settings that override the default settings for testing."""

    # Override database settings for testing
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sila_test"
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sila_test"
    PRISMA_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sila_test"

    # Connection pool settings
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800
    DATABASE_ECHO: bool = False

    # Disable rate limiting in tests
    RATE_LIMIT_ENABLED: bool = False

    # Disable external services in tests
    SEND_EMAILS: bool = False

    # Test mode settings
    testing: bool = True  # ✅ atualizado para minúsculo (Pydantic v2)

    # Disable security features that might interfere with testing
    SECURE_COOKIES: bool = False
    SECURE_HEADERS: bool = False


# Create a test settings instance
test_settings = TestSettings()


def test_testing_flag_is_true():
    """Quick check to validate that testing flag is being set correctly."""
    assert test_settings.testing is True, "Expected `testing` to be True in test settings"
