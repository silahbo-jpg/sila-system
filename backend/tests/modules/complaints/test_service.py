"""Testes de unidade para o serviço de reclamações."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone


# Módulos de teste
from app.modules.complaints.services import ComplaintService
from app.modules.complaints.models import (
    ComplaintCreate, ComplaintUpdate, 
    ComplaintCommentCreate, ComplaintCommentResponse,
    ComplaintCategoryCreate, ComplaintResponse
)


# Fixtures
@pytest.fixture
def mock_db_session():
    """Cria uma sessão de banco de dados mockada."""
    return AsyncMock()


@pytest.fixture
def complaint_service(mock_db_session):
    """Cria uma instância do serviço de reclamações com sessão mockada."""
    return ComplaintService(mock_db_session)


@pytest.fixture
def sample_complaint_data():
    """Retorna dados de exemplo para uma nova reclamação."""
    return {
        "title": "Buraco na rua",
        "description": "Buraco grande na avenida",
        "category": "infraestrutura",
        "priority": "alta"
    }


# Testes
class TestComplaintService:
    """Testes para o serviço de reclamações."""
    
    async def test_create_complaint(self, complaint_service, mock_db_session, sample_complaint_data):
        """Testa a criação de uma nova reclamação."""
        # Configura o mock
        mock_db_session.execute.return_value = MagicMock(scalar_one_or_none=lambda: None)
        mock_db_session.commit = AsyncMock()
        
        # Cria a reclamação
        result = await complaint_service.create_complaint(
            complaint_data=ComplaintCreate(**sample_complaint_data),
            user_id=1
        )
        
        # Verifica o resultado
        assert isinstance(result, dict)
        assert result["title"] == sample_complaint_data["title"]
        assert result["status"] == "aberta"  # Status padrão
        assert result["user_id"] == 1
        
        # Verifica se o commit foi chamado
        mock_db_session.commit.assert_awaited_once()


    async def test_get_complaints(self, complaint_service, mock_db_session):
        """Testa a listagem de reclamações."""
        # Dados de exemplo
        complaint_data = {
            "id": 1,
            "title": "Buraco na rua",
            "description": "Buraco grande na avenida",
            "status": "aberta",
            "category": "infraestrutura",
            "priority": "alta",
            "user_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Configura o mock
        mock_result = MagicMock()
        mock_result.mappings.return_value = [complaint_data]
        mock_db_session.execute.return_value = mock_result
        
        # Obtém as reclamações
        result = await complaint_service.get_complaints()
        
        # Verifica o resultado
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["title"] == complaint_data["title"]


    async def test_add_comment(self, complaint_service, mock_db_session):
        """Testa a adição de um comentário a uma reclamação."""
        # Dados de exemplo
        comment_data = {
            "comment": "Este é um comentário de teste",
            "is_internal": False
        }
        
        # Configura o mock
        mock_db_session.execute.return_value = MagicMock(scalar_one_or_none=lambda: {"id": 1})
        mock_db_session.commit = AsyncMock()
        
        # Adiciona o comentário
        result = await complaint_service.create_comment(
            complaint_id=1,
            comment_data=ComplaintCommentCreate(**comment_data),
            user_id=1
        )
        
        # Verifica o resultado
        assert isinstance(result, dict)
        assert result["comment"] == comment_data["comment"]
        assert result["complaint_id"] == 1
        assert result["user_id"] == 1
        
        # Verifica se o commit foi chamado
        mock_db_session.commit.assert_awaited_once()


    async def test_update_complaint_status(self, complaint_service, mock_db_session):
        """Testa a atualização do status de uma reclamação."""
        # Dados de exemplo
        update_data = {"status": "em_andamento"}
        
        # Configura o mock
        mock_db_session.execute.return_value = MagicMock(scalar_one_or_none=lambda: {"id": 1})
        mock_db_session.commit = AsyncMock()
        
        # Atualiza o status
        result = await complaint_service.update_complaint(
            complaint_id=1,
            update_data=ComplaintUpdate(**update_data)
        )
        
        # Verifica o resultado
        assert isinstance(result, dict)
        assert result["status"] == update_data["status"]
        
        # Verifica se o commit foi chamado
        mock_db_session.commit.assert_awaited_once()


# Executa os testes diretamente
if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__] + sys.argv[1:]))

