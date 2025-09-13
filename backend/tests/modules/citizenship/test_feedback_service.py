"""
Testes automatizados para o serviço de feedback do módulo de Cidadania.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
import uuid

from fastapi import status
from sqlalchemy.orm import Session

from app.modules.citizenship import services, schemas, models

# Dados de teste
TEST_USER_ID = str(uuid.uuid4())
TEST_CITIZEN_ID = str(uuid.uuid4())
TEST_FEEDBACK = {
    "tipo": "sugestao",
    "titulo": "Melhoria na interface",
    "descricao": "Sugestão para melhorar a usabilidade do sistema",
    "classificacao": 5,
    "cidadao_id": TEST_CITIZEN_ID
}

# Fixture para o banco de dados em memória
@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    return db

# Fixture para o serviço de feedback
@pytest.fixture
def feedback_service(mock_db):
    return services.FeedbackService(db=mock_db, current_user_id=TEST_USER_ID)

# Testes para o FeedbackService
class TestFeedbackService:
    def test_create_feedback(self, feedback_service, mock_db):
        # Configuração do teste
        feedback_data = schemas.FeedbackCreate(**TEST_FEEDBACK)
        mock_request = MagicMock()
        mock_request.client.host = "192.168.1.1"
        mock_request.headers.get.return_value = "Test postgres Agent"
        
        # Configura o mock para retornar um feedback com ID
        mock_feedback = models.Feedback(
            id=str(uuid.uuid4()),
            **feedback_data.dict(),
            usuario_id=TEST_USER_ID,
            status=schemas.StatusFeedbackEnum.PENDENTE,
            ip_address=mock_request.client.host,
            user_agent=mock_request.headers.get("user-agent"),
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )
        
        # Configura o mock do banco de dados
        mock_db.add.side_effect = lambda x: setattr(x, 'id', mock_feedback.id)
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Executa o teste
        result = feedback_service.create_feedback(feedback_data, mock_request)
        
        # Verificações
        assert result is not None
        assert result.id == mock_feedback.id
        assert result.titulo == TEST_FEEDBACK["titulo"]
        assert result.descricao == TEST_FEEDBACK["descricao"]
        assert result.status == schemas.StatusFeedbackEnum.PENDENTE
        assert result.ip_address == mock_request.client.host
        assert result.user_agent == mock_request.headers.get("user-agent")
        
        # Verifica se os métodos do banco de dados foram chamados corretamente
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_get_feedback(self, feedback_service, mock_db):
        # Configuração do teste
        feedback_id = str(uuid.uuid4())
        mock_feedback = models.Feedback(
            id=feedback_id,
            **TEST_FEEDBACK,
            usuario_id=TEST_USER_ID,
            status=schemas.StatusFeedbackEnum.PENDENTE,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )
        
        # Configura o mock do banco de dados
        mock_db.query.return_value.filter.return_value.first.return_value = mock_feedback
        
        # Executa o teste
        result = feedback_service.get_feedback(feedback_id)
        
        # Verificações
        assert result is not None
        assert result.id == feedback_id
        assert result.titulo == TEST_FEEDBACK["titulo"]
        
        # Verifica se a query foi construída corretamente
        mock_db.query.assert_called_with(models.Feedback)
        mock_db.query.return_value.filter.assert_called_once()
    
    def test_list_feedbacks(self, feedback_service, mock_db):
        # Configuração do teste
        feedbacks = [
            models.Feedback(
                id=str(uuid.uuid4()),
                **TEST_FEEDBACK,
                usuario_id=TEST_USER_ID,
                status=schemas.StatusFeedbackEnum.PENDENTE,
                criado_em=datetime.utcnow() - timedelta(days=1),
                atualizado_em=datetime.utcnow()
            ),
            models.Feedback(
                id=str(uuid.uuid4()),
                **{**TEST_FEEDBACK, "tipo": "problema", "titulo": "Erro no cadastro"},
                usuario_id=TEST_USER_ID,
                status=schemas.StatusFeedbackEnum.EM_ANALISE,
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow()
            )
        ]
        
        # Configura o mock do banco de dados
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = len(feedbacks)
        mock_query.offset.return_value.limit.return_value.all.return_value = feedbacks
        mock_db.query.return_value = mock_query
        
        # Executa o teste
        result, total = feedback_service.list_feedbacks()
        
        # Verificações
        assert len(result) == 2
        assert total == 2
        assert isinstance(result[0], models.Feedback)
        assert result[0].titulo in [f.titulo for f in feedbacks]
        
        # Verifica se a query foi construída corretamente
        mock_db.query.assert_called_with(models.Feedback)
        mock_query.count.assert_called_once()
        mock_query.offset.assert_called_with(0)
        mock_query.offset.return_value.limit.assert_called_with(100)
    
    def test_update_feedback(self, feedback_service, mock_db):
        # Configuração do teste
        feedback_id = str(uuid.uuid4())
        update_data = schemas.FeedbackUpdate(
            status=schemas.StatusFeedbackEnum.RESOLVIDO,
            resposta="Obrigado pelo seu feedback!"
        )
        
        # Cria um feedback simulado para ser retornado pelo get_feedback
        mock_feedback = models.Feedback(
            id=feedback_id,
            **TEST_FEEDBACK,
            usuario_id=TEST_USER_ID,
            status=schemas.StatusFeedbackEnum.PENDENTE,
            criado_em=datetime.utcnow() - timedelta(days=1),
            atualizado_em=datetime.utcnow() - timedelta(days=1)
        )
        
        # Configura o mock do banco de dados
        mock_db.query.return_value.filter.return_value.first.return_value = mock_feedback
        
        # Executa o teste
        result = feedback_service.update_feedback(feedback_id, update_data)
        
        # Verificações
        assert result is not None
        assert result.status == update_data.status
        assert result.resposta == update_data.resposta
        assert result.atualizado_em > result.criado_em
        
        # Verifica se os métodos do banco de dados foram chamados corretamente
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_delete_feedback(self, feedback_service, mock_db):
        # Configuração do teste
        feedback_id = str(uuid.uuid4())
        
        # Configura o mock do banco de dados
        mock_db.query.return_value.filter.return_value.first.return_value = models.Feedback(
            id=feedback_id,
            **TEST_FEEDBACK,
            usuario_id=TEST_USER_ID,
            status=schemas.StatusFeedbackEnum.PENDENTE
        )
        
        # Executa o teste
        result = feedback_service.delete_feedback(feedback_id)
        
        # Verificações
        assert result is True
        
        # Verifica se os métodos do banco de dados foram chamados corretamente
        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_delete_nonexistent_feedback(self, feedback_service, mock_db):
        # Configuração do teste
        feedback_id = str(uuid.uuid4())
        
        # Configura o mock do banco de dados para retornar None (feedback não encontrado)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Executa o teste
        result = feedback_service.delete_feedback(feedback_id)
        
        # Verificações
        assert result is False
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()

# Testes de validação
class TestFeedbackValidation:
    def test_create_feedback_with_invalid_rating(self, feedback_service, mock_db):
        # Configuração do teste com classificação inválida
        invalid_data = {**TEST_FEEDBACK, "classificacao": 6}  # Classificação deve ser entre 1 e 5
        
        with pytest.raises(ValueError) as exc_info:
            feedback_data = schemas.FeedbackCreate(**invalid_data)
            mock_request = MagicMock()
            feedback_service.create_feedback(feedback_data, mock_request)
        
        assert "classificacao" in str(exc_info.value)
    
    def test_create_feedback_with_missing_required_fields(self, feedback_service, mock_db):
        # Configuração do teste sem campos obrigatórios
        invalid_data = {"tipo": "sugestao"}  # Faltando título e descrição
        
        with pytest.raises(ValueError) as exc_info:
            feedback_data = schemas.FeedbackCreate(**invalid_data)
            mock_request = MagicMock()
            feedback_service.create_feedback(feedback_data, mock_request)
        
        assert "titulo" in str(exc_info.value) or "descricao" in str(exc_info.value)

