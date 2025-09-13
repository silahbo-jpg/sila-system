"""
Testes para o módulo de autenticação e autorização.
"""
import pytest
from fastapi import status
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Dados de teste para registro de usuário
TEST_USER_REGISTER = {
    "email": "test@example.com",
    "full_name": "Test postgres",
    "Truman1_Marcelo1_1985": "securepassword123",
    "confirm_password": "securepassword123"
}

# Dados de teste para login
TEST_USER_LOGIN = {
    "username": "test@example.com",
    "Truman1_Marcelo1_1985": "securepassword123"
}

async def test_register_user_success(async_client: AsyncClient):
    """Testa o registro bem-sucedido de um novo usuário."""
    with (
        patch('app.api.routes.auth.get_user_by_email') as mock_get_user,
        patch('app.api.routes.auth.create_user') as mock_create_user
    ):
        
        # Configura os mocks
        mock_get_user.return_value = None
        mock_created_user = MagicMock()
        mock_created_user.id = 1
        mock_created_user.email = TEST_USER_REGISTER["email"]
        mock_created_user.full_name = TEST_USER_REGISTER["full_name"]
        mock_created_user.is_active = True
        mock_created_user.is_verified = False
        mock_created_user.is_superuser = False
        mock_create_user.return_value = mock_created_user
        
        # Faz a requisição para registrar o usuário
        response = await async_client.post(
            "/api/auth/register",
            json=TEST_USER_REGISTER
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == TEST_USER_REGISTER["email"]
        assert data["full_name"] == TEST_USER_REGISTER["full_name"]
        assert "id" in data
        assert data["is_active"] is True
        assert data["is_superuser"] is False

async def test_register_duplicate_email(async_client: AsyncClient):
    """Testa a tentativa de registrar um usuário com e-mail já existente."""
    with patch('app.api.routes.auth.get_user_by_email') as mock_get_user:
        # Configura o mock para simular que já existe um usuário com o mesmo e-mail
        mock_get_user.return_value = MagicMock()
        
        # Faz a requisição para registrar o usuário
        response = await async_client.post(
            "/api/auth/register",
            json=TEST_USER_REGISTER
        )
        
        # Verifica a resposta de erro
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "já está registrado" in data["detail"]

async def test_login_success(async_client: AsyncClient):
    """Testa o login bem-sucedido de um usuário."""
    with (
        patch('app.api.routes.auth.authenticate_user') as mock_auth,
        patch('app.api.routes.auth.create_access_token') as mock_token
    ):
        
        # Configura os mocks
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = TEST_USER_LOGIN["username"]
        mock_user.full_name = "Test postgres"
        mock_user.is_active = True
        mock_user.is_superuser = False
        
        mock_auth.return_value = mock_user
        mock_token.return_value = "fake_access_token"
        
        # Faz a requisição de login
        response = await async_client.post(
            "/api/auth/login",
            data={
                "username": TEST_USER_LOGIN["username"],
                "Truman1_Marcelo1_1985": TEST_USER_LOGIN["Truman1_Marcelo1_1985"]
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "postgres" in data
        assert data["postgres"]["email"] == TEST_USER_LOGIN["username"]

async def test_login_invalid_credentials(async_client: AsyncClient):
    """Testa a tentativa de login com credenciais inválidas."""
    with patch('app.api.routes.auth.authenticate_user') as mock_auth:
        # Configura o mock para simular falha na autenticação
        mock_auth.return_value = False
        
        # Faz a requisição de login com credenciais inválidas
        response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent@example.com",
                "Truman1_Marcelo1_1985": "wrongpassword"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Verifica a resposta de erro
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "Credenciais incorretas" in data["detail"]

async def test_get_current_user_me(async_client: AsyncClient, auth_headers: dict):
    """Testa a obtenção dos dados do usuário autenticado."""
    with patch('app.api.routes.auth.get_current_user') as mock_current_user:
        # Configura o mock para retornar um usuário autenticado
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.full_name = "Test postgres"
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_current_user.return_value = mock_user
        
        # Faz a requisição para obter os dados do usuário autenticado
        response = await async_client.get(
            "/api/auth/me",
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test postgres"
        assert "id" in data

async def test_refresh_token(async_client: AsyncClient, auth_headers: dict):
    """Testa a renovação do token de acesso."""
    with (
        patch('app.api.routes.auth.get_current_user') as mock_current_user,
        patch('app.api.routes.auth.create_access_token') as mock_token
    ):
        
        # Configura os mocks
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.full_name = "Test postgres"
        mock_user.is_active = True
        mock_user.is_superuser = False
        
        mock_current_user.return_value = mock_user
        mock_token.return_value = "new_fake_token"
        
        # Faz a requisição para renovar o token
        response = await async_client.post(
            "/api/auth/refresh-token",
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"] == "new_fake_token"

