"""Testes de integração para os endpoints do módulo de reclamações."""
import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch, MagicMock

# Importa a configuração de teste isolado
from .test_config import client

# Módulos de teste
from app.modules.complaints.models import (
    ComplaintCreate, ComplaintUpdate, ComplaintResponse,
    ComplaintCommentCreate, ComplaintCommentResponse,
    ComplaintCategoryCreate, ComplaintCategoryResponse,
    ComplaintFilter, ComplaintStats
)


# Fixtures
@pytest.fixture
def mock_complaint_service():
    """Fixture para mock do serviço de reclamações."""
    with patch('app.modules.complaints.endpoints.get_complaint_service') as mock_service:
        yield mock_service


@pytest.fixture
def mock_auth():
    """Fixture para mock de autenticação."""
    with patch('app.modules.complaints.endpoints.get_current_user') as mock_user:
        mock_user.return_value = {"id": 1, "username": "testuser", "roles": ["postgres"]}
        yield mock_user


# Dados de teste
@pytest.fixture
def sample_complaint():
    """Retorna um exemplo de reclamação para testes."""
    return {
        "id": 1,
        "title": "Buraco na rua",
        "description": "Buraco grande na avenida",
        "status": "aberta",
        "category": "infraestrutura",
        "priority": "alta",
        "user_id": 1,
        "created_at": "2023-10-01T10:00:00",
        "updated_at": "2023-10-01T10:00:00"
    }


@pytest.fixture
def sample_comment():
    """Retorna um exemplo de comentário para testes."""
    return {
        "id": 1,
        "complaint_id": 1,
        "user_id": 1,
        "comment": "Este é um comentário de teste",
        "is_internal": False,
        "created_at": "2023-10-01T10:00:00"
    }


# Testes para o endpoint de listagem de reclamações


def test_list_complaints(test_client, mock_complaint_service, sample_complaint):
    """Testa o endpoint de listagem de reclamações."""
    # Configura o mock do serviço
    mock_service_instance = AsyncMock()
    mock_service_instance.get_complaints.return_value = [sample_complaint]
    mock_complaint_service.return_value = mock_service_instance
    
    # Faz a requisição
    response = test_client.get("/api/complaints/")
    
    # Verifica a resposta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == sample_complaint["title"]
    mock_service_instance.get_complaints.assert_called_once()


# Testes para o endpoint de criação de reclamação


def test_create_complaint(test_client, mock_complaint_service, sample_complaint):
    """Testa o endpoint de criação de reclamação."""
    # Configura o mock do serviço
    mock_service_instance = AsyncMock()
    mock_service_instance.create_complaint.return_value = sample_complaint
    mock_complaint_service.return_value = mock_service_instance
    
    # Dados para a requisição
    complaint_data = {
        "title": "Buraco na rua",
        "description": "Buraco grande na avenida",
        "category": "infraestrutura",
        "priority": "alta",
        "location": "Avenida Principal, 123"
    }
    
    # Faz a requisição
    response = test_client.post("/api/complaints/", json=complaint_data)
    
    # Verifica a resposta
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == complaint_data["title"]
    assert data["status"] == "aberta"
    mock_service_instance.create_complaint.assert_called_once()


# Testes para o endpoint de adição de comentário


def test_add_comment(test_client, mock_complaint_service, sample_comment):
    """Testa o endpoint de adição de comentário a uma reclamação."""
    # Configura o mock do serviço
    mock_service_instance = AsyncMock()
    mock_service_instance.create_comment.return_value = sample_comment
    mock_complaint_service.return_value = mock_service_instance
    
    # Dados para a requisição
    comment_data = {
        "comment": "Este é um comentário de teste",
        "is_internal": False
    }
    
    # Faz a requisição
    response = test_client.post("/api/complaints/1/comments", json=comment_data)
    
    # Verifica a resposta
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["comment"] == comment_data["comment"]
    assert data["complaint_id"] == 1
    assert data["user_id"] == 1
    mock_service_instance.create_comment.assert_called_once()


# Testes para o endpoint de atualização de status


def test_update_status(test_client, mock_complaint_service, sample_complaint):
    """Testa o endpoint de atualização de status de uma reclamação."""
    # Configura o mock do serviço
    mock_service_instance = AsyncMock()
    updated_complaint = sample_complaint.copy()
    updated_complaint["status"] = "em_andamento"
    updated_complaint["updated_at"] = "2023-10-01T11:00:00"
    mock_service_instance.update_complaint.return_value = updated_complaint
    mock_complaint_service.return_value = mock_service_instance
    
    # Dados para a requisição
    update_data = {
        "status": "em_andamento"
    }
    
    # Faz a requisição
    response = test_client.patch("/api/complaints/1/status", json=update_data)
    
    # Verifica a resposta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "em_andamento"
    mock_service_instance.update_complaint.assert_called_once()


# Testes para erros de validação


def test_validation_error(test_client):
    """Testa erros de validação nos endpoints."""
    # Teste de criação com dados inválidos
    invalid_data = {
        "title": "",  # Título vazio
        "description": "",  # Descrição vazia
        "category": "inexistente"  # Categoria inválida
    }
    
    response = test_client.post("/api/complaints/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Verifica as mensagens de erro
    errors = response.json()["detail"]
    assert any("title" in str(e) for e in errors)
    assert any("description" in str(e) for e in errors)
    assert any("category" in str(e) for e in errors)


# Testes para autenticação/autorização


def test_unauthorized_access(test_client):
    """Testa acesso não autorizado aos endpoints protegidos."""
    # Tenta acessar sem token
    response = test_client.get("/api/complaints/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # Tenta acessar com token inválido
    response = test_client.get(
        "/api/complaints/",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

