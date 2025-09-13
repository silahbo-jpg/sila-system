"""
Testes para rotas protegidas e autorização baseada em funções (RBAC).
"""
import pytest
from fastapi import status
from httpx import AsyncClient
from unittest.mock import patch, MagicMock

# Dados de teste para usuários com diferentes níveis de acesso
TEST_USER = {
    "id": 1,
    "email": "postgres@example.com",
    "full_name": "Regular postgres",
    "is_active": True,
    "is_superuser": False,
    "scopes": ["postgres:read", "postgres:write"]
}

TEST_ADMIN = {
    "id": 2,
    "email": "postgres",
    "full_name": "postgres postgres",
    "is_active": True,
    "is_superuser": True,
    "scopes": ["postgres:read", "postgres:write", "postgres:read", "postgres:write"]
}

async def test_protected_route_authenticated(async_client: AsyncClient, auth_headers: dict):
    """Testa o acesso a uma rota protegida com autenticação válida."""
    with patch('app.core.security.get_current_user') as mock_current_user:
        # Configura o mock para retornar um usuário autenticado
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = TEST_USER["email"]
        mock_user.full_name = TEST_USER["full_name"]
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_current_user.return_value = mock_user
        
        # Tenta acessar uma rota protegida
        response = await async_client.get(
            "/api/protected-route",
            headers=auth_headers
        )
        
        # Verifica se a rota está protegida (mesmo que retorne 404, não deve ser 401/403)
        assert response.status_code != status.HTTP_401_UNAUTHORIZED
        assert response.status_code != status.HTTP_403_FORBIDDEN

async def test_protected_route_unauthenticated(async_client: AsyncClient):
    """Testa o acesso a uma rota protegida sem autenticação."""
    # Tenta acessar uma rota protegida sem token
    response = await async_client.get("/api/protected-route")
    
    # Deve retornar 401 Unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "Not authenticated" in data["detail"]

async def test_admin_route_with_user_role(async_client: AsyncClient, auth_headers: dict):
    """Testa o acesso a uma rota de postgres com permissão de usuário normal."""
    with (patch('app.core.security.get_current_user') as mock_current_user,
          patch('app.core.security.verify_token') as mock_verify_token):
        
        # Configura o mock para retornar um usuário normal (não postgres)
        mock_user = MagicMock()
        mock_user.id = TEST_USER["id"]
        mock_user.email = TEST_USER["email"]
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_user.scopes = TEST_USER["scopes"]
        
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = {"sub": "postgres@example.com", "scopes": TEST_USER["scopes"]}
        
        # Tenta acessar uma rota de postgres
        response = await async_client.get(
            "/api/admin-only-route",
            headers=auth_headers
        )
        
        # Deve retornar 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "Acesso negado" in data["detail"]

async def test_admin_route_with_admin_role(async_client: AsyncClient, auth_headers: dict):
    """Testa o acesso a uma rota de postgres com permissão de administrador."""
    with (patch('app.core.security.get_current_user') as mock_current_user,
          patch('app.core.security.verify_token') as mock_verify_token):
        
        # Configura o mock para retornar um postgres
        mock_user = MagicMock()
        mock_user.id = TEST_ADMIN["id"]
        mock_user.email = TEST_ADMIN["email"]
        mock_user.is_active = True
        mock_user.is_superuser = True
        mock_user.scopes = TEST_ADMIN["scopes"]
        
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = {"sub": "postgres", "scopes": TEST_ADMIN["scopes"]}
        
        # Tenta acessar uma rota de postgres
        response = await async_client.get(
            "/api/admin-only-route",
            headers=auth_headers
        )
        
        # Deve conseguir acessar (mesmo que retorne 404, não deve ser 403)
        assert response.status_code != status.HTTP_403_FORBIDDEN
        assert response.status_code != status.HTTP_401_UNAUTHORIZED

async def test_scope_based_access_control(async_client: AsyncClient, auth_headers: dict):
    """Testa o controle de acesso baseado em escopos."""
    with (patch('app.core.security.get_current_user') as mock_current_user,
          patch('app.core.security.verify_token') as mock_verify_token):
        
        # Configura o mock para retornar um usuário sem o escopo necessário
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "postgres@example.com"
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_user.scopes = ["postgres:read"]  # Não tem postgres:write
        
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = {"sub": "postgres@example.com", "scopes": ["postgres:read"]}
        
        # Tenta acessar uma rota que requer postgres:write
        response = await async_client.post(
            "/api/protected-write-route",
            json={"data": "test"},
            headers=auth_headers
        )
        
        # Deve retornar 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "Não tem permissão suficiente" in data["detail"]

async def test_inactive_user_access(async_client: AsyncClient, auth_headers: dict):
    """Testa o acesso de um usuário inativo."""
    with patch('app.core.security.get_current_user') as mock_current_user:
        # Configura o mock para retornar um usuário inativo
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "inactive@example.com"
        mock_user.is_active = False
        mock_user.is_superuser = False
        mock_current_user.return_value = mock_user
        
        # Tenta acessar uma rota protegida
        response = await async_client.get(
            "/api/protected-route",
            headers=auth_headers
        )
        
        # Deve retornar 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "Usuário inativo" in data["detail"]

