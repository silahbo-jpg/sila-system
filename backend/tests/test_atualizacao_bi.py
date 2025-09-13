"""
Tests for BI update endpoints.
"""
import os
import sys
import logging
import pytest
from fastapi.testclient import TestClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mark all tests in this module as integration tests
pytestmark = [
    pytest.mark.integration,
    pytest.mark.citizenship,
    pytest.mark.bi_updates,
    pytest.mark.skip(reason="Temporarily skipping all tests for debugging")
]
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, AsyncMock

from app.main import app
from app.db.session import Base, get_db, TestingSessionLocal
from app.core.security import get_password_hash, create_access_token
from app.core.auth.security import get_current_user, get_current_active_user
from app.modules.citizenship.models.atualizacao_b_i import AtualizacaoBI
from app.modules.auth.models.user import User, UserRole

# Test user data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword"
TEST_ADMIN_EMAIL = "admin@example.com"
TEST_ADMIN_PASSWORD = "adminpassword"

# Test data for creating/updating BI updates
TEST_BI_UPDATE_DATA = {
    "nome_completo": "Maria Silva",
    "numero_documento": "987654321LA123",
    "tipo_documento": "Bilhete de Identidade",
    "data_nascimento": "1990-01-01",
    "morada": "Avenida Nova, 456, Luanda",
    "telefone": "912345678",
    "email": "maria@example.com",
    "motivo_atualizacao": "Primeira emissão",
    "status": "pendente"
}

TEST_BI_UPDATE_UPDATE = {
    "status": "em_analise",
    "observacoes": "Em análise pela equipe técnica"
}

# Client fixture with overridden dependencies
@pytest.fixture(scope="function")
def client():
    # Create a new FastAPI app for testing
    from fastapi import FastAPI
    from app.api.api_v1.api import api_router
    
    test_app = FastAPI()
    test_app.include_router(api_router, prefix="/api")
    
    # Override the get_db dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # Override the get_current_user dependency
    def override_get_current_user():
        return {"id": 1, "email": "test@example.com", "is_active": True, "is_superuser": False}
    
    # Apply the overrides
    test_app.dependency_overrides[get_db] = override_get_db
    test_app.dependency_overrides[get_current_active_user] = override_get_current_user
    
    with TestClient(test_app) as c:
        yield c
    
    # Clear overrides after test
    test_app.dependency_overrides.clear()

# Database session fixture
@pytest.fixture(scope="function")
def db_session():
    # Setup test database
    from app.db.session import engine, TestingSessionLocal, Base
    
    # Drop all tables first to ensure a clean state
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = TestingSessionLocal()
    
    # Begin a transaction
    transaction = db.begin()
    
    try:
        yield db
        # Rollback the transaction after the test
        transaction.rollback()
    finally:
        # Close the session
        db.close()
        # Clean up
        Base.metadata.drop_all(bind=engine)

# Test user fixture
@pytest.fixture(scope="function")
def test_user(db_session: Session):
    # Delete any existing users to avoid conflicts
    db_session.query(User).delete()
    
    # Create test user
    user = User(
        email=TEST_USER_EMAIL,
        hashed_password=get_password_hash(TEST_USER_PASSWORD),
        full_name="Test User",
        role=UserRole.USER,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# Test admin user fixture
@pytest.fixture(scope="function")
def test_admin(db_session: Session):
    # Create admin user
    admin = User(
        email=TEST_ADMIN_EMAIL,
        hashed_password=get_password_hash(TEST_ADMIN_PASSWORD),
        full_name="Test Admin",
        role=UserRole.ADMIN,
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

# Test BI update request fixture
@pytest.fixture(scope="function")
def test_bi_update(db_session: Session, test_user: User):
    # Delete any existing BI updates to avoid conflicts
    db_session.query(AtualizacaoBI).delete()
    
    # Create test BI update
    bi_update = AtualizacaoBI(
        nome_completo="João da Silva",
        numero_documento="123456789LA123",
        tipo_documento="Bilhete de Identidade",
        data_nascimento=datetime.now() - timedelta(days=25*365),
        morada="Rua Teste, 123, Luanda",
        telefone="923456789",
        email=test_user.email,
        motivo_atualizacao="Atualização de morada",
        status="pendente",
        user_id=test_user.id,
        dados_adicionais={"comprovativo_morada": "doc1.pdf"},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(bi_update)
    db_session.commit()
    db_session.refresh(bi_update)
    return bi_update

# Authentication token fixtures
@pytest.fixture(scope="function")
def user_token(test_user: User):
    return create_access_token(subject=test_user.email)

@pytest.fixture(scope="function")
def admin_token(test_admin: User):
    return create_access_token(subject=test_admin.email)

# Authentication header fixtures
@pytest.fixture(scope="function")
def user_auth_headers(user_token: str):
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture(scope="function")
def admin_auth_headers(admin_token: str):
    return {"Authorization": f"Bearer {admin_token}"}

# Test data for creating/updating BI updates
TEST_BI_UPDATE_DATA = {
    "nome_completo": "Maria Silva",
    "numero_documento": "987654321LA123",
    "tipo_documento": "Bilhete de Identidade",
    "data_nascimento": "1990-01-01",
    "morada": "Avenida Nova, 456, Luanda",
    "telefone": "912345678",
    "email": "maria@example.com",
    "motivo_atualizacao": "Primeira emissão",
    "status": "pendente"
}

TEST_BI_UPDATE_UPDATE = {
    "status": "em_analise",
    "observacoes": "Em análise pela equipa técnica"
}

class TestCreateBIUpdate:
    """Test cases for creating BI update requests"""
    
    @pytest.mark.skip(reason="Temporarily skipping for debugging")
    def test_create_bi_update_success(self, client: TestClient, test_user: User, db_session: Session):
        """Test creating a new BI update request"""
        logger.info("Starting test_create_bi_update_success")
        
        try:
            # Mock the current user
            with patch('app.core.auth.security.get_current_user') as mock_user:
                logger.info("Setting up mock user")
                mock_user.return_value = {
                    "id": test_user.id,
                    "email": test_user.email,
                    "is_active": True,
                    "is_superuser": False
                }
                
                # Create test data
                test_data = TEST_BI_UPDATE_DATA.copy()
                logger.info(f"Test data: {test_data}")
                
                # Make the request
                logger.info("Making POST request to /api/bi-updates/")
                response = client.post("/api/bi-updates/", json=test_data)
                logger.info(f"Response status code: {response.status_code}")
                logger.info(f"Response content: {response.text}")
                
                # Verify the response
                assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
                data = response.json()
                assert data["nome_completo"] == test_data["nome_completo"]
                assert data["status"] == "pendente"
                
                # Verify the data was saved to the database
                logger.info("Verifying database entry")
                bi_update = db_session.query(AtualizacaoBI).filter(
                    AtualizacaoBI.numero_documento == test_data["numero_documento"]
                ).first()
                assert bi_update is not None, "BI update was not saved to the database"
                assert bi_update.user_id == test_user.id, f"Expected user_id {test_user.id}, got {bi_update.user_id}"
                
                logger.info("test_create_bi_update_success completed successfully")
                
        except Exception as e:
            logger.error(f"Test failed with error: {str(e)}")
            logger.exception("Test failed with exception:")
            raise
    
    def test_create_bi_update_missing_required_field(self, client: TestClient, test_user: User):
        """Test creating a BI update with missing required fields"""
        # Mock the current user
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            # Missing required field 'nome_completo'
            invalid_data = TEST_BI_UPDATE_DATA.copy()
            del invalid_data["nome_completo"]
            
            response = client.post("/api/bi-updates/", json=invalid_data)
            assert response.status_code == 422
            assert "field required" in response.text.lower()


class TestGetBIUpdate:
    """Test cases for retrieving BI update requests"""
    
    def test_get_bi_update_success(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User):
        """Test retrieving an existing BI update request"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.get(f"/api/bi-updates/{test_bi_update.id}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == test_bi_update.id
            assert data["nome_completo"] == test_bi_update.nome_completo
    
    def test_get_bi_update_not_found(self, client: TestClient, test_user: User):
        """Test retrieving a non-existent BI update request"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.get("/api/bi-updates/9999")
            assert response.status_code == 404
    
    def test_get_bi_update_unauthorized(self, client: TestClient, test_bi_update: AtualizacaoBI):
        """Test retrieving a BI update request that doesn't belong to the user"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": 9999,  # Different user ID
                "email": "other@example.com",
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.get(f"/api/bi-updates/{test_bi_update.id}")
            assert response.status_code == 403


class TestListBIUpdates:
    """Test cases for listing BI update requests"""
    
    def test_list_bi_updates_success(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User):
        """Test listing BI update requests"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.get("/api/bi-updates/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert any(item["id"] == test_bi_update.id for item in data)
    
    def test_list_bi_updates_filter_by_status(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User):
        """Test filtering BI update requests by status"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.get("/api/bi-updates/?status=pendente")
            
            assert response.status_code == 200
            data = response.json()
            assert all(item["status"] == "pendente" for item in data)
    
    def test_list_bi_updates_pagination(self, client: TestClient, test_user: User, db_session: Session):
        """Test pagination of BI update requests"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            # Create test data
            for i in range(15):
                bi_update = AtualizacaoBI(
                    nome_completo=f"User {i}",
                    numero_documento=f"12345678{i:02d}LA123",
                    tipo_documento="Bilhete de Identidade",
                    data_nascimento=datetime.now() - timedelta(days=25*365),
                    morada=f"Rua Teste {i}, Luanda",
                    telefone=f"92345678{i}",
                    email=f"user{i}@example.com",
                    motivo_atualizacao=f"Test {i}",
                    status="pendente",
                    user_id=test_user.id
                )
                db_session.add(bi_update)
            db_session.commit()
            
            # Test first page
            response = client.get("/api/bi-updates/?skip=0&limit=10")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 10
            
            # Test second page
            response = client.get("/api/bi-updates/?skip=10&limit=10")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 5  # Only 5 remaining


class TestUpdateBIUpdate:
    """Test cases for updating BI update requests"""
    
    def test_update_bi_update_success(self, client: TestClient, test_bi_update: AtualizacaoBI, test_admin_user: User, db_session: Session):
        """Test updating a BI update request as admin"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_admin_user.id,
                "email": test_admin_user.email,
                "is_active": True,
                "is_superuser": True
            }
            
            update_data = {
                "status": "em_analise",
                "observacoes": "Em análise pela equipe técnica"
            }
            
            response = client.put(
                f"/api/bi-updates/{test_bi_update.id}",
                json=update_data
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "em_analise"
            assert data["observacoes"] == "Em análise pela equipe técnica"
            
            # Verify the update in the database
            db_session.refresh(test_bi_update)
            assert test_bi_update.status == "em_analise"
            assert test_bi_update.observacoes == "Em análise pela equipe técnica"
    
    def test_update_bi_update_unauthorized(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User):
        """Test updating a BI update request as non-admin"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.put(
                f"/api/bi-updates/{test_bi_update.id}",
                json={"status": "em_analise"}
            )
            
            assert response.status_code == 403
    
    def test_update_nonexistent_bi_update(self, client: TestClient, test_admin_user: User):
        """Test updating a non-existent BI update request"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_admin_user.id,
                "email": test_admin_user.email,
                "is_active": True,
                "is_superuser": True
            }
            
            response = client.put(
                "/api/bi-updates/9999",
                json={"status": "em_analise"}
            )
            assert response.status_code == 404


class TestDeleteBIUpdate:
    """Test cases for deleting/canceling BI update requests"""
    
    def test_cancel_bi_update_success(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User, db_session: Session):
        """Test canceling a BI update request"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.delete(
                f"/api/bi-updates/{test_bi_update.id}?razao=Teste de cancelamento"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "cancelado"
            
            # Verify the status was updated in the database
            db_session.refresh(test_bi_update)
            assert test_bi_update.status == "cancelado"
    
    def test_delete_bi_update_admin(self, client: TestClient, test_bi_update: AtualizacaoBI, test_admin_user: User, db_session: Session):
        """Test admin hard-deleting a BI update request"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_admin_user.id,
                "email": test_admin_user.email,
                "is_active": True,
                "is_superuser": True
            }
            
            # First cancel the request
            test_bi_update.status = "cancelado"
            db_session.add(test_bi_update)
            db_session.commit()
            
            # Now delete it
            response = client.delete(
                f"/api/bi-updates/{test_bi_update.id}?hard_delete=true"
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Pedido eliminado com sucesso"
            
            # Verify it's gone from the database
            bi_update = db_session.query(AtualizacaoBI).filter(
                AtualizacaoBI.id == test_bi_update.id
            ).first()
            assert bi_update is None
    
    def test_delete_bi_update_unauthorized(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User):
        """Test deleting a BI update request without admin privileges"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            response = client.delete(
                f"/api/bi-updates/{test_bi_update.id}?hard_delete=true"
            )
            
            # Should return 403 Forbidden for non-admin
            assert response.status_code == 403
            assert "message" in response.json()


class TestFileUploads:
    """Test cases for file uploads with BI update requests"""
    
    def test_upload_document_success(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User, db_session: Session):
        """Test uploading a document with a BI update request"""
        with patch('app.core.auth.security.get_current_user') as mock_user, \
             patch('app.core.storage.save_uploaded_file') as mock_save, \
             patch('app.modules.citizenship.services.atualizacao_bi_service.add_document_to_bi_update') as mock_add_doc:
            
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            # Mock the file save and document addition
            test_file = ("test.pdf", b"test content", "application/pdf")
            mock_save.return_value = "path/to/uploaded/test.pdf"
            test_bi_update.documentos = ["path/to/uploaded/test.pdf"]
            mock_add_doc.return_value = test_bi_update
            
            response = client.post(
                f"/api/bi-updates/{test_bi_update.id}/documents",
                files={"file": test_file}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "documentos" in data
            assert len(data["documentos"]) > 0
            assert "test.pdf" in data["documentos"][0]
    
    def test_upload_invalid_file_type(self, client: TestClient, test_bi_update: AtualizacaoBI, test_user: User):
        """Test uploading an invalid file type"""
        with patch('app.core.auth.security.get_current_user') as mock_user:
            mock_user.return_value = {
                "id": test_user.id,
                "email": test_user.email,
                "is_active": True,
                "is_superuser": False
            }
            
            test_file = ("test.exe", b"malicious content", "application/octet-stream")
            
            response = client.post(
                f"/api/bi-updates/{test_bi_update.id}/documents",
                files={"file": test_file}
            )
            
            assert response.status_code == 400
            assert "Invalid file type" in response.text
        assert "detail" in response.json()
        assert "Tipo de ficheiro não suportado" in response.json()["detail"]
