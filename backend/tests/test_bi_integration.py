"""
Integration tests for BI update functionality.
"""
import os
import sys
import logging
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import app and models
from app.main import app
from app.modules.auth.models.user import User, UserRole
from app.modules.citizenship.models.atualizacao_b_i import AtualizacaoBI
from app.core.security import get_password_hash

# Test data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword"
TEST_BI_UPDATE_DATA = {
    "nome_completo": "Maria Silva",
    "numero_documento": "987654321LA123",
    "tipo_documento": "Bilhete de Identidade",
    "data_nascimento": "1990-01-01",
    "morada": "Avenida Teste, 456, Luanda",
    "telefone": "912345678",
    "email": "maria.silva@example.com",
    "motivo_atualizacao": "Atualização de dados pessoais"
}

logger.info("Test data initialized")

# Database setup
@pytest.fixture(scope="module")
async def engine():
    """Create a test database engine."""
    from app.core.config import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    
    # Use a separate test database
    test_db_url = settings.ASYNC_DATABASE_URL.replace("/sila_dev", "/sila_test")
    engine = create_async_engine(
        test_db_url,
        echo=True,
        future=True,
        pool_pre_ping=True
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture(scope="module")
async def db_session(engine):
    """Create a test database session."""
    from sqlalchemy.ext.asyncio import AsyncSession
    
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()

@pytest.fixture(scope="module")
def test_client(engine):
    """Create a test client with overridden dependencies."""
    from fastapi import FastAPI
    from app.api.api_v1.api import api_router
    
    # Create a new FastAPI app for testing
    test_app = FastAPI()
    test_app.include_router(api_router, prefix="/api")
    
    # Override the get_db dependency
    def override_get_db():
        try:
            TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # Override the get_current_user dependency
    def override_get_current_user():
        return {"id": 1, "email": TEST_USER_EMAIL, "is_active": True, "is_superuser": False}
    
    # Apply the overrides
    from app.db.session import get_db
    from app.core.auth.security import get_current_active_user
    
    test_app.dependency_overrides[get_db] = override_get_db
    test_app.dependency_overrides[get_current_active_user] = override_get_current_user
    
    with TestClient(test_app) as client:
        yield client
    
    # Clear overrides after test
    test_app.dependency_overrides.clear()

# Tests
@pytest.mark.asyncio
async def test_create_bi_update(test_client, test_user, db_session):
    """Test creating a new BI update request."""
    logger.info("Testing BI update creation...")
    
    # Make the request
    response = test_client.post("/api/bi-updates/", json=TEST_BI_UPDATE_DATA)
    
    # Verify the response
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    data = response.json()
    
    # Verify the response data
    assert data["nome_completo"] == TEST_BI_UPDATE_DATA["nome_completo"]
    assert data["status"] == "pendente"
    
    # Verify the data was saved to the database
    from sqlalchemy import select
    
    result = await db_session.execute(
        select(AtualizacaoBI).where(
            AtualizacaoBI.numero_documento == TEST_BI_UPDATE_DATA["numero_documento"]
        )
    )
    bi_update = result.scalars().first()
    
    assert bi_update is not None, "BI update was not saved to the database"
    assert bi_update.user_id == test_user.id, f"Expected user_id {test_user.id}, got {bi_update.user_id}"
    
    logger.info("✓ BI update creation test passed")

@pytest.mark.asyncio
async def test_get_bi_update(test_client, test_user, db_session):
    """Test retrieving a BI update request."""
    logger.info("Testing BI update retrieval...")
    
    # Create a test BI update
    bi_update = AtualizacaoBI(
        user_id=test_user.id,
        **TEST_BI_UPDATE_DATA,
        status="pendente",
        data_criacao=datetime.utcnow()
    )
    
    db_session.add(bi_update)
    await db_session.commit()
    await db_session.refresh(bi_update)
    
    # Make the request
    response = test_client.get(f"/api/bi-updates/{bi_update.id}")
    
    # Verify the response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    
    # Verify the response data
    assert data["id"] == bi_update.id
    assert data["nome_completo"] == bi_update.nome_completo
    
    logger.info("✓ BI update retrieval test passed")

if __name__ == "__main__":
    # Run tests directly for debugging
    logger.info("Running tests directly...")
    
    def engine():
        """Create a test database engine."""
        logger.info("Creating test database engine...")
        # Use an in-memory SQLite database for testing
        TEST_DATABASE_URL = "sqlite:///:memory:"
        logger.debug(f"Using test database URL: {TEST_DATABASE_URL}")
        
        try:
            engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
            logger.info("Successfully created database engine")
            
            # Log database URL and engine info
            logger.debug(f"Database engine: {engine}")
            logger.debug(f"Database URL: {engine.url}")
            
            # Create all tables
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Successfully created database tables")
            
            # Log all tables that were created
            table_names = Base.metadata.tables.keys()
            logger.debug(f"Created tables: {', '.join(table_names) if table_names else 'No tables found'}")
            
            return engine
        except Exception as e:
            logger.error(f"Failed to create test database engine: {e}")
            raise
    
    # Create a test session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine())
    db = TestingSessionLocal()
    
    try:
        # Create test user
        from app.modules.auth.models.user import User
        from app.core.security import get_password_hash
        
        # Delete any existing test user
        db.query(User).filter(User.email == TEST_USER_EMAIL).delete()
        
        user = User(
            email=TEST_USER_EMAIL,
            hashed_password=get_password_hash(TEST_USER_PASSWORD),
            is_active=True,
            is_superuser=False,
            full_name="Test User"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Created test user with ID: {user.id}")
        
        # Run tests
        import pytest
        pytest.main([__file__, "-v"])
        
    finally:
        # Clean up
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        logger.info("Cleaned up test database")
