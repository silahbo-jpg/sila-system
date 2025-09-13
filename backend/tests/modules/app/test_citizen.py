"""
Testes para o módulo de cidadania.
"""
import pytest
from fastapi import status
from httpx import AsyncClient
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

# Dados de teste para criar um cidadão
TEST_CITIZEN_DATA = {
    "full_name": "João Pedro da Silva",
    "bi_number": "003456789LA045",
    "cpf": "12345678901",
    "birth_date": "1990-01-15",
    "gender": "Masculino",
    "marital_status": "Solteiro(a)",
    "phone": "923456789",
    "email": "joao.silva@example.com",
    "nationality": "Angolana",
    "province": "Luanda",
    "municipality": "Belas",
    "commune": "Maianga",
    "neighborhood": "Bairro Popular",
    "street": "Rua da Liberdade",
    "house_number": "42"
}

# Dados de teste para atualizar um cidadão
UPDATED_CITIZEN_DATA = {
    "full_name": "João Pedro da Silva Santos",
    "phone": "924567890",
    "email": "joao.santos@example.com"
}

async def test_create_citizen_success(async_client: AsyncClient, auth_headers: dict):
    """Testa a criação bem-sucedida de um cidadão."""
    with patch('app.modules.citizenship.crud.create_citizen') as mock_create:
        # Configura o mock para retornar um cidadão criado
        mock_citizen = MagicMock()
        mock_citizen.dict.return_value = {"id": 1, **TEST_CITIZEN_DATA}
        mock_create.return_value = mock_citizen
        
        # Faz a requisição para criar o cidadão
        response = await async_client.post(
            "/api/citizenship/citizens/",
            json=TEST_CITIZEN_DATA,
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["full_name"] == TEST_CITIZEN_DATA["full_name"]
        assert data["bi_number"] == TEST_CITIZEN_DATA["bi_number"]
        assert "id" in data

async def test_create_citizen_duplicate_bi(async_client: AsyncClient, auth_headers: dict):
    """Testa a tentativa de criar um cidadão com BI duplicado."""
    with (patch('app.modules.citizenship.crud.get_citizen_by_bi') as mock_get_bi,
          patch('app.modules.citizenship.crud.create_citizen') as mock_create):
        
        # Configura o mock para simular que já existe um cidadão com o mesmo BI
        mock_get_bi.return_value = MagicMock()
        
        # Faz a requisição para criar o cidadão
        response = await async_client.post(
            "/api/citizenship/citizens/",
            json=TEST_CITIZEN_DATA,
            headers=auth_headers
        )
        
        # Verifica a resposta de erro
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "Já existe um cidadão com este número de BI" in data["detail"]

async def test_get_citizen_success(async_client: AsyncClient, auth_headers: dict):
    """Testa a obtenção de um cidadão existente."""
    with patch('app.modules.citizenship.crud.get_citizen') as mock_get:
        # Configura o mock para retornar um cidadão
        mock_citizen = MagicMock()
        mock_citizen.dict.return_value = {"id": 1, **TEST_CITIZEN_DATA}
        mock_get.return_value = mock_citizen
        
        # Faz a requisição para obter o cidadão
        response = await async_client.get(
            "/api/citizenship/citizens/1",
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["full_name"] == TEST_CITIZEN_DATA["full_name"]

async def test_get_citizen_not_found(async_client: AsyncClient, auth_headers: dict):
    """Testa a tentativa de obter um cidadão que não existe."""
    with patch('app.modules.citizenship.crud.get_citizen') as mock_get:
        # Configura o mock para retornar None (cidadão não encontrado)
        mock_get.return_value = None
        
        # Faz a requisição para obter um cidadão inexistente
        response = await async_client.get(
            "/api/citizenship/citizens/999",
            headers=auth_headers
        )
        
        # Verifica a resposta de erro
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "Cidadão não encontrado" in data["detail"]

async def test_update_citizen_success(async_client: AsyncClient, auth_headers: dict):
    """Testa a atualização de um cidadão existente."""
    with (patch('app.modules.citizenship.crud.get_citizen') as mock_get,
          patch('app.modules.citizenship.crud.update_citizen') as mock_update):
        
        # Configura os mocks
        mock_citizen = MagicMock()
        mock_citizen.dict.return_value = {"id": 1, **TEST_CITIZEN_DATA, **UPDATED_CITIZEN_DATA}
        
        mock_get.return_value = mock_citizen
        mock_update.return_value = mock_citizen
        
        # Faz a requisição para atualizar o cidadão
        response = await async_client.put(
            "/api/citizenship/citizens/1",
            json=UPDATED_CITIZEN_DATA,
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == UPDATED_CITIZEN_DATA["full_name"]
        assert data["phone"] == UPDATED_CITIZEN_DATA["phone"]

async def test_delete_citizen_success(async_client: AsyncClient, auth_headers: dict):
    """Testa a remoção de um cidadão existente."""
    with (patch('app.modules.citizenship.crud.get_citizen') as mock_get,
          patch('app.modules.citizenship.crud.delete_citizen') as mock_delete):
        
        # Configura os mocks
        mock_citizen = MagicMock()
        mock_citizen.dict.return_value = {"id": 1, **TEST_CITIZEN_DATA}
        
        mock_get.return_value = mock_citizen
        mock_delete.return_value = mock_citizen
        
        # Faz a requisição para remover o cidadão
        response = await async_client.delete(
            "/api/citizenship/citizens/1",
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["full_name"] == TEST_CITIZEN_DATA["full_name"]

async def test_delete_citizen_not_found(async_client: AsyncClient, auth_headers: dict):
    """Testa a tentativa de remover um cidadão que não existe."""
    with patch('app.modules.citizenship.crud.get_citizen') as mock_get:
        # Configura o mock para retornar None (cidadão não encontrado)
        mock_get.return_value = None
        
        # Faz a requisição para remover um cidadão inexistente
        response = await async_client.delete(
            "/api/citizenship/citizens/999",
            headers=auth_headers
        )
        
        # Verifica a resposta de erro
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "Cidadão não encontrado" in data["detail"]

async def test_list_citizens_success(async_client: AsyncClient, auth_headers: dict):
    """Testa a listagem de cidadãos com paginação."""
    with patch('app.modules.citizenship.crud.get_citizens') as mock_list:
        # Configura o mock para retornar uma lista de cidadãos
        mock_citizens = [
            MagicMock(dict=MagicMock(return_value={"id": i, **TEST_CITIZEN_DATA, "full_name": f"Cidadão {i}"}))
            for i in range(1, 4)
        ]
        mock_list.return_value = (mock_citizens, 3)  # Lista e total
        
        # Faz a requisição para listar os cidadãos
        response = await async_client.get(
            "/api/citizenship/citizens/",
            params={"skip": 0, "limit": 10},
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert "id" in data[0]
        assert "full_name" in data[0]

async def test_unauthorized_access(async_client: AsyncClient):
    """Testa o acesso não autorizado a um endpoint protegido."""
    # Tenta acessar sem token de autenticação
    response = await async_client.get("/api/citizenship/citizens/1")
    
    # Verifica a resposta de erro
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "Not authenticated" in data["detail"]

