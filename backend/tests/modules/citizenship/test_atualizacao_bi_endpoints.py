"""
Testes para os endpoints de atualização de BI no módulo de cidadania.
"""
import pytest
from fastapi import status
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Test data
TEST_BI_UPDATE = {
    "nome_completo": "João da Silva",
    "numero_documento": "123456789LA123",
    "tipo_documento": "Bilhete de Identidade",
    "data_nascimento": "1990-01-01",
    "morada": "Rua Teste, 123, Luanda",
    "telefone": "923456789",
    "email": "joao.silva@example.com",
    "motivo_atualizacao": "Atualização de morada",
    "status": "pendente"
}

def setup_mocks(mock_client):
    """Configura os mocks para simular autenticação e banco de dados."""
    # Mock para get_current_user
    from app.core.auth.security import get_current_user
    from app.modules.auth.models.user import User
    
    # Cria um usuário de teste
    test_user = User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=False
    )
    
    # Mock para get_current_user
    mock_client.app.dependency_overrides[get_current_user] = lambda: test_user
    
    # Mock para get_db
    from app.db.session import get_db
    mock_db = MagicMock(spec=Session)
    mock_client.app.dependency_overrides[get_db] = lambda: mock_db
    
    return test_user, mock_db

@pytest.mark.asyncio
async def test_create_bi_update(client):
    """Testa a criação de um novo pedido de atualização de BI."""
    test_user, mock_db = setup_mocks(client)
    
    # Configura o mock para o serviço
    with patch('app.modules.citizenship.services.atualizacao_bi_service.create_bi_update_request') as mock_create:
        # Configura o retorno do mock
        mock_create.return_value = {
            "id": 1,
            **TEST_BI_UPDATE,
            "user_id": test_user.id,
            "data_criacao": datetime.now().isoformat()
        }
        
        # Faz a requisição
        response = client.post(
            "/api/bi-updates/",
            json=TEST_BI_UPDATE,
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 1
        assert data["nome_completo"] == TEST_BI_UPDATE["nome_completo"]
        assert data["status"] == "pendente"

@pytest.mark.asyncio
async def test_get_bi_update(client):
    """Testa a obtenção de um pedido de atualização de BI."""
    test_user, mock_db = setup_mocks(client)
    
    # Configura o mock para o serviço
    with patch('app.modules.citizenship.services.atualizacao_bi_service.get_bi_update_by_id') as mock_get:
        # Configura o retorno do mock
        mock_get.return_value = {
            "id": 1,
            **TEST_BI_UPDATE,
            "user_id": test_user.id,
            "data_criacao": (datetime.now() - timedelta(days=1)).isoformat()
        }
        
        # Faz a requisição
        response = client.get(
            "/api/bi-updates/1",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["nome_completo"] == TEST_BI_UPDATE["nome_completo"]

@pytest.mark.asyncio
async def test_list_bi_updates(client):
    """Testa a listagem de pedidos de atualização de BI."""
    test_user, mock_db = setup_mocks(client)
    
    # Configura o mock para o serviço
    with patch('app.modules.citizenship.services.atualizacao_bi_service.list_bi_updates') as mock_list:
        # Configura o retorno do mock
        mock_list.return_value = [
            {
                "id": 1,
                **TEST_BI_UPDATE,
                "user_id": test_user.id,
                "data_criacao": (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                "id": 2,
                **TEST_BI_UPDATE,
                "nome_completo": "Maria Silva",
                "user_id": 2,
                "data_criacao": (datetime.now() - timedelta(days=2)).isoformat()
            }
        ]
        
        # Faz a requisição
        response = client.get(
            "/api/bi-updates/",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2

@pytest.mark.asyncio
async def test_update_bi_update(client):
    """Testa a atualização de um pedido de atualização de BI."""
    test_user, mock_db = setup_mocks(client)
    
    # Dados de atualização
    update_data = {
        "status": "em_analise",
        "observacoes": "Em análise pela equipe técnica"
    }
    
    # Configura o mock para o serviço
    with patch('app.modules.citizenship.services.atualizacao_bi_service.update_bi_update_request') as mock_update:
        # Configura o retorno do mock
        mock_update.return_value = {
            "id": 1,
            **TEST_BI_UPDATE,
            **update_data,
            "user_id": test_user.id,
            "data_criacao": (datetime.now() - timedelta(days=1)).isoformat(),
            "data_atualizacao": datetime.now().isoformat()
        }
        
        # Faz a requisição
        response = client.put(
            "/api/bi-updates/1",
            json=update_data,
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["status"] == "em_analise"
        assert data["observacoes"] == "Em análise pela equipe técnica"

@pytest.mark.asyncio
async def test_cancel_bi_update(client):
    """Testa o cancelamento de um pedido de atualização de BI."""
    test_user, mock_db = setup_mocks(client)
    
    # Configura o mock para o serviço
    with patch('app.modules.citizenship.services.atualizacao_bi_service.delete_bi_update') as mock_delete:
        # Configura o retorno do mock
        mock_delete.return_value = {
            "id": 1,
            **TEST_BI_UPDATE,
            "status": "cancelado",
            "user_id": test_user.id,
            "data_criacao": (datetime.now() - timedelta(days=1)).isoformat(),
            "data_cancelamento": datetime.now().isoformat()
        }
        
        # Faz a requisição
        response = client.delete(
            "/api/bi-updates/1?razao=Teste+de+cancelamento",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["status"] == "cancelado"

@pytest.mark.asyncio
async def test_upload_document(client):
    """Testa o upload de documento para um pedido de atualização de BI."""
    test_user, mock_db = setup_mocks(client)
    
    # Configura o mock para o serviço de arquivos
    with patch('app.core.storage.save_uploaded_file') as mock_save_file, \
         patch('app.modules.citizenship.services.atualizacao_bi_service.get_bi_update_by_id') as mock_get_bi:
        
        # Configura os retornos dos mocks
        mock_save_file.return_value = "path/to/uploaded/document.pdf"
        mock_get_bi.return_value = {
            "id": 1,
            **TEST_BI_UPDATE,
            "user_id": test_user.id,
            "documentos": []
        }
        
        # Cria um arquivo de teste
        test_file = ("test.pdf", b"test content", "application/pdf")
        
        # Faz a requisição
        response = client.post(
            "/api/bi-updates/1/documents",
            files={"file": test_file},
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "documentos" in data
        assert len(data["documentos"]) > 0
