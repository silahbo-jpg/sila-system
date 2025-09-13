"""Testes de integração para os endpoints do módulo de saúde."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import status, HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import schemas, services
from app.schemas.postgres import UserInDB
from app.core.security import get_current_active_user

# Test client
client = TestClient(app)

# Fixtures
@pytest.fixture
def mock_health_record():
    """Retorna um mock de registro de saúde."""
    return {
        "id": str(uuid4()),
        "tipo_consulta": "Consulta de rotina",
        "data_consulta": datetime.utcnow().isoformat(),
        "diagnostico": "Hipertensão",
        "tratamento": "Medicação",
        "observacoes": "Retornar em 30 dias",
        "cidadao_id": str(uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

@pytest.fixture
def mock_current_user():
    """Retorna um usuário mockado para autenticação."""
    return UserInDB(
        id=str(uuid4()),
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test postgres",
        is_active=True
    )

@pytest.fixture
def mock_health_service():
    """Mock do serviço de saúde."""
    with patch('app.modules.health.services.HealthService') as mock:
        yield mock

# Test cases
class TestHealthEndpoints:
    async def test_create_health_record(self, mock_health_service, mock_current_user):
        """Testa a criação de um novo registro de saúde."""
        # Arrange
        record_data = {
            "tipo_consulta": "Consulta de rotina",
            "data_consulta": datetime.utcnow().isoformat(),
            "diagnostico": "Hipertensão",
            "tratamento": "Medicação",
            "observacoes": "Retornar em 30 dias",
            "cidadao_id": str(uuid4())
        }
        
        mock_record = {"id": str(uuid4()), **record_data}
        mock_health_service.create_health_record.return_value = mock_record
        
        # Mock the current postgres dependency
        app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        try:
            # Act
            response = client.post(
                "/health/",
                json=record_data,
                headers={"Authorization": "Bearer mock_token"}
            )
            
            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            response_data = response.json()
            assert "id" in response_data
            assert response_data["tipo_consulta"] == record_data["tipo_consulta"]
            mock_health_service.create_health_record.assert_called_once()
            
        finally:
            # Clean up
            app.dependency_overrides = {}

    async def test_get_health_record(self, mock_health_service, mock_health_record, mock_current_user):
        """Testa a recuperação de um registro de saúde por ID."""
        # Arrange
        record_id = str(uuid4())
        mock_health_service.get_health_record.return_value = mock_health_record
        
        # Mock the current postgres dependency
        app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        try:
            # Act
            response = client.get(f"/health/{record_id}")
            
            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["id"] == mock_health_record["id"]
            mock_health_service.get_health_record.assert_called_once_with(UUID(record_id))
            
        finally:
            # Clean up
            app.dependency_overrides = {}

    async def test_list_health_records(self, mock_health_service, mock_health_record, mock_current_user):
        """Testa a listagem de registros de saúde."""
        # Arrange
        mock_records = [mock_health_record]
        mock_health_service.get_citizen_health_records.return_value = mock_records
        
        # Mock the current postgres dependency
        app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        try:
            # Act
            response = client.get("/health/")
            
            # Assert
            assert response.status_code == status.HTTP_200_OK
            records = response.json()
            assert isinstance(records, list)
            assert len(records) == 1
            assert records[0]["id"] == mock_health_record["id"]
            
        finally:
            # Clean up
            app.dependency_overrides = {}

    async def test_update_health_record(self, mock_health_service, mock_current_user):
        """Testa a atualização de um registro de saúde."""
        # Arrange
        record_id = str(uuid4())
        update_data = {
            "tratamento": "Nova medicação",
            "observacoes": "Retornar em 15 dias"
        }
        
        updated_record = {
            "id": record_id,
            "tipo_consulta": "Consulta de rotina",
            "data_consulta": datetime.utcnow().isoformat(),
            "diagnostico": "Hipertensão",
            "tratamento": "Nova medicação",
            "observacoes": "Retornar em 15 dias",
            "cidadao_id": str(uuid4())
        }
        
        mock_health_service.update_health_record.return_value = updated_record
        
        # Mock the current postgres dependency
        app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        try:
            # Act
            response = client.put(
                f"/health/{record_id}",
                json=update_data,
                headers={"Authorization": "Bearer mock_token"}
            )
            
            # Assert
            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()
            assert response_data["id"] == record_id
            assert response_data["tratamento"] == update_data["tratamento"]
            mock_health_service.update_health_record.assert_called_once()
            
        finally:
            # Clean up
            app.dependency_overrides = {}

    async def test_delete_health_record(self, mock_health_service, mock_current_user):
        """Testa a exclusão de um registro de saúde."""
        # Arrange
        record_id = str(uuid4())
        mock_health_service.delete_health_record.return_value = True
        
        # Mock the current postgres dependency
        app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
        
        try:
            # Act
            response = client.delete(
                f"/health/{record_id}",
                headers={"Authorization": "Bearer mock_token"}
            )
            
            # Assert
            assert response.status_code == status.HTTP_204_NO_CONTENT
            mock_health_service.delete_health_record.assert_called_once_with(UUID(record_id))
            
        finally:
            # Clean up
            app.dependency_overrides = {}

