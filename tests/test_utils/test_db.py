"""Test database utilities."""
import os
from typing import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.db.database import Base

# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:Truman1_Marcelo1_1985@localhost:5432/test_sila"
)

# Create test database engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def init_test_db():
    """Initialize the test database with all tables."""
    Base.metadata.create_all(bind=test_engine)

def drop_test_db():
    """Drop all tables from the test database."""
    Base.metadata.drop_all(bind=test_engine)

def get_test_db() -> Generator[Session, None, None]:
    """Dependency to get a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def test_db_engine():
    ""
    Create a test database and return the engine.
    The database is dropped after all tests are done.
    """
    # Create all tables
    init_test_db()
    
    yield test_engine
    
    # Clean up
    drop_test_db()

@pytest.fixture(scope="function")
def db_session(test_db_engine):
    """
    Create a new database session with a rollback at the end of the test.
    """
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
