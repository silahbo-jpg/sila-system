"""
Testes automatizados para os endpoints de feedback do módulo de Cidadania.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
import uuid
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.models.postgres import postgres
from app.modules.citizenship import models, schemas

# Dados de teste
TEST_USER_ID = str(uuid.uuid4())
TEST_ADMIN_ID = str(uuid.uuid4())
TEST_CITIZEN_ID = str(uuid.uuid4())
TEST_FEEDBACK = {
    "tipo": "sugestao",
    "titulo": "Melhoria na interface",
    "descricao": "Sugestão para melhorar a usabilidade do sistema",
    "classificacao": 5,
    "cidadao_id": TEST_CITIZEN_ID
}

# Fixture para o cliente de teste
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

# Fixture para usuário autenticado
@pytest.fixture
def auth_user():
    postgres = postgres(
        id=TEST_USER_ID,
        email="test@example.com",
        full_name="Test postgres",
        is_active=True,
        is_superuser=False
    )
    return postgres

# Fixture para administrador autenticado
@pytest.fixture
def admin_user():
    postgres = postgres(
        id=TEST_ADMIN_ID,
        email="postgres",
        full_name="postgres postgres",
        is_active=True,
        is_superuser=True
    )
    return postgres

# Fixture para mock do serviço de feedback
@pytest.fixture
def mock_feedback_service():
    with patch('app.modules.citizenship.services.FeedbackService') as mock:
        yield mock

# Testes para os endpoints de feedback
class TestFeedbackEndpoints:
    def test_create_feedback_authenticated(self, client, auth_user, mock_feedback_service):
        # Configuração do mock
        feedback_id = str(uuid.uuid4())
        created_feedback = models.Feedback(
            id=feedback_id,
            **TEST_FEEDBACK,
            usuario_id=auth_user.id,
            status=schemas.StatusFeedbackEnum.PENDENTE,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )
        mock_feedback_service.return_value.create_feedback.return_value = created_feedback
        
        # Executa o teste
        with patch('app.core.security.get_current_active_user', return_value=auth_user):
            response = client.post(
                "/api/citizenship/feedback/",
                json=TEST_FEEDBACK,
                headers={"X-Test-Request": "true"}
            )
        
        # Verificações
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == feedback_id
        assert data["titulo"] == TEST_FEEDBACK["titulo"]
        assert data["status"] == "pendente"
        
        # Verifica se o serviço foi chamado corretamente
        mock_feedback_service.return_value.create_feedback.assert_called_once()
        call_args = mock_feedback_service.return_value.create_feedback.call_args[0]
        assert isinstance(call_args[0], schemas.FeedbackCreate)
        assert call_args[0].titulo == TEST_FEEDBACK["titulo"]
    
    def test_list_feedbacks_as_admin(self, client, admin_user, mock_feedback_service):
        # Configuração do mock
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
        
        mock_feedback_service.return_value.list_feedbacks.return_value = (feedbacks, 2)
        
        # Executa o teste como administrador
        with patch('app.core.security.get_current_active_user', return_value=admin_user):
            response = client.get(
                "/api/citizenship/feedback/",
                params={"status": "pendente"},
                headers={"X-Test-Request": "true"}
            )
        
        # Verificações
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 2
        assert data["total"] == 2
        assert data["items"][0]["titulo"] in [f.titulo for f in feedbacks]
        
        # Verifica se o serviço foi chamado corretamente
        mock_feedback_service.return_value.list_feedbacks.assert_called_once_with(
            status=schemas.StatusFeedbackEnum.PENDENTE,
            tipo=None,
            cidadao_id=None,
            skip=0,
            limit=100
        )
    
    def test_get_feedback(self, client, auth_user, mock_feedback_service):
        # Configuração do mock
        feedback_id = str(uuid.uuid4())
        feedback = models.Feedback(
            id=feedback_id,
            **TEST_FEEDBACK,
            usuario_id=auth_user.id,  # O feedback pertence ao usuário autenticado
            status=schemas.StatusFeedbackEnum.PENDENTE,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )
        mock_feedback_service.return_value.get_feedback.return_value = feedback
        
        # Executa o teste
        with patch('app.core.security.get_current_active_user', return_value=auth_user):
            response = client.get(f"/api/citizenship/feedback/{feedback_id}")
        
        # Verificações
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == feedback_id
        assert data["titulo"] == TEST_FEEDBACK["titulo"]
        
        # Verifica se o serviço foi chamado corretamente
        mock_feedback_service.return_value.get_feedback.assert_called_once_with(feedback_id)
    
    def test_update_feedback_as_admin(self, client, admin_user, mock_feedback_service):
        # Configuração do mock
        feedback_id = str(uuid.uuid4())
        update_data = {
            "status": "resolvido",
            "resposta": "Obrigado pelo seu feedback!"
        }
        
        updated_feedback = models.Feedback(
            id=feedback_id,
            **TEST_FEEDBACK,
            status=schemas.StatusFeedbackEnum.RESOLVIDO,
            resposta=update_data["resposta"],
            usuario_id=TEST_USER_ID,  # Outro usuário
            criado_em=datetime.utcnow() - timedelta(days=1),
            atualizado_em=datetime.utcnow()
        )
        
        mock_feedback_service.return_value.update_feedback.return_value = updated_feedback
        
        # Executa o teste como administrador
        with patch('app.core.security.get_current_active_user', return_value=admin_user):
            response = client.patch(
                f"/api/citizenship/feedback/{feedback_id}",
                json=update_data
            )
        
        # Verificações
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == feedback_id
        assert data["status"] == "resolvido"
        assert data["resposta"] == update_data["resposta"]
        
        # Verifica se o serviço foi chamado corretamente
        mock_feedback_service.return_value.update_feedback.assert_called_once()
        call_args = mock_feedback_service.return_value.update_feedback.call_args[0]
        assert call_args[0] == feedback_id
        assert isinstance(call_args[1], schemas.FeedbackUpdate)
        assert call_args[1].status == schemas.StatusFeedbackEnum.RESOLVIDO
    
    def test_delete_feedback_as_admin(self, client, admin_user, mock_feedback_service):
        # Configuração do mock
        feedback_id = str(uuid.uuid4())
        mock_feedback_service.return_value.delete_feedback.return_value = True
        
        # Executa o teste como administrador
        with patch('app.core.security.get_current_active_user', return_value=admin_user):
            response = client.delete(f"/api/citizenship/feedback/{feedback_id}")
        
        # Verificações
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verifica se o serviço foi chamado corretamente
        mock_feedback_service.return_value.delete_feedback.assert_called_once_with(feedback_id)

# Testes de autorização e validação
class TestFeedbackAuthorization:
    def test_create_feedback_unauthenticated(self, client, mock_feedback_service):
        # Executa o teste sem autenticação
        response = client.post(
            "/api/citizenship/feedback/",
            json=TEST_FEEDBACK
        )
        
        # Deve retornar 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_feedbacks_as_regular_user(self, client, auth_user, mock_feedback_service):
        # Configura o mock para retornar apenas os feedbacks do usuário
        feedbacks = [
            models.Feedback(
                id=str(uuid.uuid4()),
                **TEST_FEEDBACK,
                usuario_id=auth_user.id,  # Apenas feedbacks do usuário autenticado
                status=schemas.StatusFeedbackEnum.PENDENTE,
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow()
            )
        ]
        
        mock_feedback_service.return_value.list_feedbacks.return_value = (feedbacks, 1)
        
        # Executa o teste como usuário regular
        with patch('app.core.security.get_current_active_user', return_value=auth_user):
            response = client.get("/api/citizenship/feedback/")
        
        # Verificações
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["usuario_id"] == auth_user.id
        
        # Verifica se o serviço foi chamado com o ID do usuário atual
        mock_feedback_service.return_value.list_feedbacks.assert_called_once()
        call_args = mock_feedback_service.return_value.list_feedbacks.call_args[1]
        assert call_args["usuario_id"] == auth_user.id
    
    def test_update_feedback_as_regular_user(self, client, auth_user, mock_feedback_service):
        # Configuração do mock para simular que o feedback pertence a outro usuário
        feedback_id = str(uuid.uuid4())
        update_data = {"status": "resolvido"}
        
        # Executa o teste como usuário regular tentando atualizar feedback de outro usuário
        with patch('app.core.security.get_current_active_user', return_value=auth_user), \
             patch('app.modules.citizenship.services.FeedbackService.get_feedback') as mock_get:
            
            # Configura o mock para retornar um feedback de outro usuário
            other_user_id = str(uuid.uuid4())
            mock_feedback = models.Feedback(
                id=feedback_id,
                **TEST_FEEDBACK,
                usuario_id=other_user_id,  # Outro usuário
                status=schemas.StatusFeedbackEnum.PENDENTE
            )
            mock_get.return_value = mock_feedback
            
            response = client.patch(
                f"/api/citizenship/feedback/{feedback_id}",
                json=update_data
            )
        
        # Deve retornar 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verifica se o serviço de atualização não foi chamado
        mock_feedback_service.return_value.update_feedback.assert_not_called()

