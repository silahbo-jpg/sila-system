"""Testes para os serviços do módulo de Cidadania."""


import pytest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch, AsyncMock
from pytest_mock import mocker
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.citizenship import services, schemas, models
from app.core.exceptions import ValidationException


# Fixtures


@pytest.fixture
def mock_db_session():
    """Cria uma sessão mock do banco de dados."""

    return MagicMock(spec=Session)


@pytest.fixture
def current_user_id():
    """Retorna um ID de usuário para testes."""

    return uuid.uuid4()


@pytest.fixture
def citizenship_service(mock_db_session, current_user_id):
    """Cria uma instância do serviço de cidadania para testes."""

    return services.CitizenshipService(db=mock_db_session, current_user_id=current_user_id)


# Testes para CitizenshipService


class TestCitizenshipService:
    """Testes para o serviço de cidadania."""


    def test_register_citizen_success(self, citizenship_service, mock_db_session):
        """Testa o registro bem-sucedido de um cidadão."""

        # Dados de teste
        citizen_data = schemas.CitizenCreate(
            bi_numero="123456789LA123",
            nome_completo="João da Silva",
            data_nascimento=date(1990, 1, 1),
            genero=schemas.GeneroEnum.MASCULINO,
            estado_civil=schemas.EstadoCivilEnum.SOLTEIRO,
            naturalidade="Luanda",
            municipio_residencia="Luanda",
            comuna="Maianga",
            bairro="Alvalade",
            provincia="Luanda",
            telefone_principal="+244923456789"
        )
        
        # Configura o mock do CRUD
        mock_citizen = models.Citizen(
            id=uuid.uuid4(),
            **citizen_data.dict()
        )
        
        # Configura o mock para simular a criação bem-sucedida
        citizenship_service.crud.create_citizen = MagicMock(return_value=mock_citizen)
        citizenship_service._generate_default_documents = MagicMock()
        
        # Executa o método
        result = citizenship_service.register_citizen(citizen_data)
        
        # Verifica os resultados
        assert result == mock_citizen
        citizenship_service.crud.create_citizen.assert_called_once_with(citizen_data)
        citizenship_service._generate_default_documents.assert_called_once_with(mock_citizen)


    def test_get_citizen_found(self, citizenship_service, mock_db_session):
        """Testa a busca de um cidadão existente."""

        # Configura o mock
        citizen_id = uuid.uuid4()
        mock_citizen = MagicMock()
        citizenship_service.crud.get_citizen_by_id = MagicMock(return_value=mock_citizen)
        
        # Executa o método
        result = citizenship_service.get_citizen(citizen_id)
        
        # Verifica os resultados
        assert result == mock_citizen
        citizenship_service.crud.get_citizen_by_id.assert_called_once()


    def test_get_citizen_not_found(self, citizenship_service, mock_db_session):
        """Testa a busca de um cidadão que não existe."""

        # Configura o mock para retornar None (não encontrado)
        citizen_id = uuid.uuid4()
        citizenship_service.crud.get_citizen_by_id = MagicMock(return_value=None)
        
        # Executa o método e verifica a exceção
        with pytest.raises(HTTPException) as exc_info:
            citizenship_service.get_citizen(citizen_id)
        
        # Verifica a exceção
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Cidadão não encontrado" in str(exc_info.value.detail)


    def test_search_citizens(self, citizenship_service, mock_db_session):
        """Testa a busca de cidadãos com filtros."""

        # Configura o mock
        mock_citizens = [MagicMock(), MagicMock()]
        total = 2
        citizenship_service.crud.get_multi = MagicMock(return_value=(mock_citizens, total))
        
        # Executa o método
        result, result_total = citizenship_service.search_citizens(
            query="João",
            municipality="Luanda",
            skip=0,
            limit=10
        )
        
        # Verifica os resultados
        assert result == mock_citizens
        assert result_total == total
        citizenship_service.crud.get_multi.assert_called_once()


    def test_update_citizen_success(self, citizenship_service, mock_db_session):
        """Testa a atualização bem-sucedida de um cidadão."""

        # Dados de teste
        citizen_id = uuid.uuid4()
        update_data = schemas.CitizenUpdate(
            telefone_principal="+244923333333",
            email="novo.email@example.com"
        )
        
        # Configura o mock
        mock_citizen = MagicMock()
        citizenship_service.crud.get = MagicMock(return_value=mock_citizen)
        citizenship_service.crud.update = MagicMock(return_value=mock_citizen)
        
        # Executa o método
        result = citizenship_service.update_citizen(citizen_id, update_data)
        
        # Verifica os resultados
        assert result == mock_citizen
        citizenship_service.crud.get.assert_called_once_with(citizen_id)
        citizenship_service.crud.update.assert_called_once_with(mock_citizen, update_data)


    def test_delete_citizen_success(self, citizenship_service, mock_db_session):
        """Testa a exclusão bem-sucedida de um cidadão."""

        # Dados de teste
        citizen_id = uuid.uuid4()
        
        # Configura o mock
        mock_citizen = MagicMock()
        citizenship_service.crud.get = MagicMock(return_value=mock_citizen)
        citizenship_service.crud.remove = MagicMock()
        
        # Executa o método
        citizenship_service.delete_citizen(citizen_id)
        
        # Verifica as chamadas
        citizenship_service.crud.get.assert_called_once_with(citizen_id)
        citizenship_service.crud.remove.assert_called_once_with(mock_citizen)


# Testes para FeedbackService


class TestFeedbackService:
    """Testes para o serviço de feedback."""


    @pytest.fixture
    def feedback_service(self, mock_db_session):
        """Cria uma instância do serviço de feedback para testes."""

        return services.FeedbackService(db=mock_db_session, current_user_id=uuid.uuid4())


    def test_create_feedback_success(self, feedback_service, mock_db_session):
        """Testa a criação bem-sucedida de um feedback."""

        # Dados de teste
        feedback_data = schemas.FeedbackCreate(
            tipo=schemas.TipoFeedbackEnum.SUGESTAO,
            titulo="Melhoria no atendimento",
            descricao="Sugiro ampliar o horário de atendimento.",
            classificacao=5
        )
        
        # Mock do serviço de feedback
        mocker.patch(
            "app.modules.citizenship.services.FeedbackService",
            return_value=AsyncMock()
        )
        feedback_service.db.refresh = MagicMock(side_effect=lambda x: setattr(x, 'id', uuid.uuid4()))
        
        # Executa o método
        result = feedback_service.create_feedback(feedback_data)
        
        # Verifica os resultados
        assert result is not None
        feedback_service.db.add.assert_called_once()
        feedback_service.db.commit.assert_called_once()


    def test_get_feedback_found(self, feedback_service, mock_db_session):
        """Testa a busca de um feedback existente."""

        # Configura o mock
        feedback_id = uuid.uuid4()
        mock_feedback = MagicMock()
        feedback_service.db.query.return_value.filter.return_value.first.return_value = mock_feedback
        
        # Executa o método
        result = feedback_service.get_feedback(str(feedback_id))
        
        # Verifica os resultados
        assert result == mock_feedback


    def test_update_feedback_success(self, feedback_service, mock_db_session):
        """Testa a atualização bem-sucedida de um feedback."""

        # Dados de teste
        feedback_id = uuid.uuid4()
        update_data = schemas.FeedbackUpdate(
            status=schemas.StatusFeedbackEnum.RESOLVIDO,
            resposta="Obrigado pelo seu feedback!"
        )
        
        # Configura o mock
        mock_feedback = MagicMock()
        feedback_service.get_feedback = MagicMock(return_value=mock_feedback)
        feedback_service.db.commit = MagicMock()
        
        # Executa o método
        result = feedback_service.update_feedback(str(feedback_id), update_data)
        
        # Verifica os resultados
        assert result == mock_feedback
        feedback_service.get_feedback.assert_called_once_with(str(feedback_id))
        feedback_service.db.commit.assert_called_once()


    def test_delete_feedback_success(self, feedback_service, mock_db_session):
        """Testa a exclusão bem-sucedida de um feedback."""

        # Configura o mock
        feedback_id = uuid.uuid4()
        mock_feedback = MagicMock()
        feedback_service.get_feedback = MagicMock(return_value=mock_feedback)
        feedback_service.db.delete = MagicMock()
        feedback_service.db.commit = MagicMock()
        
        # Executa o método
        result = feedback_service.delete_feedback(str(feedback_id))
        
        # Verifica os resultados
        assert result is True
        feedback_service.get_feedback.assert_called_once_with(str(feedback_id))
        feedback_service.db.delete.assert_called_once_with(mock_feedback)
        feedback_service.db.commit.assert_called_once()

