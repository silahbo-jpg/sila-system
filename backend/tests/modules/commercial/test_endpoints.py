"""Testes de integração para os endpoints do módulo commercial."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.modules.commercial import schemas
from app.modules.auth.schemas import UserInDB, UserRole


# Fixture para o cliente de teste
@pytest.fixture
def client():
    """Retorna um cliente de teste configurado."""
    return TestClient(app)


# Fixture para um usuário autenticado
@pytest.fixture
def authenticated_user():
    """Retorna um usuário autenticado para teste."""
    return UserInDB(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        role=UserRole.postgres,
        full_name="Test postgres"
    )


# Fixture para mockar a autenticação
@pytest.fixture
def auth_headers(authenticated_user):
    """Retorna headers de autenticação para teste."""
    return {"Authorization": "Bearer test_token"}


class TestCommercialEndpoints:
    """Testes para os endpoints do módulo commercial."""

    @pytest.mark.asyncio
    @patch('app.modules.commercial.endpoints.get_current_superuser')
    @patch('app.modules.commercial.crud.create_licenca')
    async def test_solicitar_licenca(
        self, 
        mock_create_licenca,
        mock_current_user,
        client,
        auth_headers,
        authenticated_user,
        mock_licenca
    ):
        """Testa a solicitação de uma nova licença comercial."""
        # Configura os mocks
        mock_current_user.return_value = authenticated_user
        mock_create_licenca.return_value = mock_licenca
        
        # Dados para a requisição
        licenca_data = {
            "nomeEmpresa": "Empresa Teste Ltda",
            "nif": "123456789",
            "atividade": "Comércio de Produtos",
            "endereco": "Rua Teste, 123",
            "validade": "2025-12-31",
            "estado": "pendente"
        }
        
        # Faz a requisição
        response = client.post(
            "/commercial/licenca/",
            json=licenca_data,
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == mock_licenca.id
        mock_create_licenca.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.modules.commercial.endpoints.get_current_user')
    @patch('app.modules.commercial.crud.get_licenca_by_id')
    async def test_obter_licenca(
        self, 
        mock_get_licenca,
        mock_current_user,
        client,
        auth_headers,
        authenticated_user,
        mock_licenca
    ):
        """Testa a obtenção de uma licença comercial por ID."""
        # Configura os mocks
        mock_current_user.return_value = authenticated_user
        mock_get_licenca.return_value = mock_licenca
        
        # ID para teste
        licenca_id = 1
        
        # Faz a requisição
        response = client.get(
            f"/commercial/licenca/{licenca_id}",
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == mock_licenca.id
        mock_get_licenca.assert_called_once_with(licenca_id)

    @pytest.mark.asyncio
    @patch('app.modules.commercial.endpoints.get_current_user')
    @patch('app.modules.commercial.crud.get_licenca_by_id')
    @patch('app.modules.commercial.services.gerar_pdf_com_qrcode')
    async def test_gerar_pdf(
        self, 
        mock_gerar_pdf,
        mock_get_licenca,
        mock_current_user,
        client,
        auth_headers,
        authenticated_user,
        mock_licenca
    ):
        """Testa a geração de PDF para uma licença comercial."""
        # Configura os mocks
        mock_current_user.return_value = authenticated_user
        mock_get_licenca.return_value = mock_licenca
        
        # Configura o mock para retornar um PDF de teste
        pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> /MediaBox [0 0 612 792] /Contents 4 0 R>>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Hello, World!) Tj ET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000053 00000 n \n0000000109 00000 n \n0000000187 00000 n \n0000000281 00000 n \ntrailer\n<< /Size 6 /postgres 1 0 R /Info << >> >>\nstartxref\n336\n%%EOF\n"
        
        mock_response = MagicMock()
        mock_response.body_iterator = [pdf_content]
        mock_gerar_pdf.return_value = mock_response
        
        # ID para teste
        licenca_id = 1
        
        # Faz a requisição
        response = client.get(
            f"/commercial/licenca/{licenca_id}/pdf",
            headers=auth_headers
        )
        
        # Verifica a resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert response.content.startswith(b"%PDF")
        mock_get_licenca.assert_called_once_with(licenca_id)
        mock_gerar_pdf.assert_called_once_with(mock_licenca)

