"""Testes para os serviços do módulo de saúde."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime

from fastapi import HTTPException, status

from app.modules.health import services, schemas, crud
from app.modules.citizenship.crud import get_cidadao


class TestHealthService:
    """Testes para a classe HealthService."""

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.create_health')
    @patch('app.modules.citizenship.crud.get_cidadao')
    async def test_create_health_record_success(
        self, 
        mock_get_cidadao,
        mock_create_health,
        mock_cidadao,
        health_create_data
    ):
        """Testa a criação bem-sucedida de um registro de saúde."""
        # Configura os mocks
        mock_get_cidadao.return_value = mock_cidadao
        
        # Cria um mock para o registro de saúde retornado pelo CRUD
        mock_health = MagicMock()
        mock_health.id = 1
        mock_create_health.return_value = mock_health
        
        # Cria o objeto de entrada
        health_in = schemas.HealthCreate(**health_create_data)
        
        # Chama o método a ser testado
        result = await services.HealthService.create_health_record(health_in)
        
        # Verifica as chamadas aos mocks
        mock_get_cidadao.assert_called_once_with(health_create_data["cidadao_id"])
        mock_create_health.assert_called_once()
        
        # Verifica o resultado
        assert result.id == 1

    @pytest.mark.asyncio
    @patch('app.modules.citizenship.crud.get_cidadao')
    async def test_create_health_record_citizen_not_found(
        self, 
        mock_get_cidadao,
        health_create_data
    ):
        """Testa a tentativa de criar registro para cidadão inexistente."""
        # Configura o mock para retornar None (cidadão não encontrado)
        mock_get_cidadao.return_value = None
        
        # Cria o objeto de entrada
        health_in = schemas.HealthCreate(**health_create_data)
        
        # Verifica se a exceção é lançada
        with pytest.raises(HTTPException) as exc_info:
            await services.HealthService.create_health_record(health_in)
        
        # Verifica o status code e a mensagem de erro
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Cidadão não encontrado" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.get_health')
    async def test_get_health_record_success(self, mock_get_health, mock_health_record):
        """Testa a busca de um registro de saúde existente."""
        # Configura o mock
        mock_get_health.return_value = mock_health_record
        
        # Chama o método a ser testado
        health_id = uuid4()
        result = await services.HealthService.get_health_record(health_id)
        
        # Verifica as chamadas aos mocks
        mock_get_health.assert_called_once_with(health_id)
        
        # Verifica o resultado
        assert result.id == mock_health_record.id

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.get_health')
    async def test_get_health_record_not_found(self, mock_get_health):
        """Testa a busca de um registro de saúde inexistente."""
        # Configura o mock para retornar None (registro não encontrado)
        mock_get_health.return_value = None
        
        # Verifica se a exceção é lançada
        health_id = uuid4()
        with pytest.raises(HTTPException) as exc_info:
            await services.HealthService.get_health_record(health_id)
        
        # Verifica o status code e a mensagem de erro
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Registro de saúde não encontrado" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.update_health')
    @patch('app.modules.health.crud.get_health')
    async def test_update_health_record_success(
        self, 
        mock_get_health,
        mock_update_health,
        mock_health_record,
        health_update_data
    ):
        """Testa a atualização bem-sucedida de um registro de saúde."""
        # Configura os mocks
        mock_get_health.return_value = mock_health_record
        mock_update_health.return_value = mock_health_record
        
        # Cria o objeto de atualização
        health_update = schemas.HealthUpdate(**health_update_data)
        health_id = uuid4()
        
        # Chama o método a ser testado
        result = await services.HealthService.update_health_record(health_id, health_update)
        
        # Verifica as chamadas aos mocks
        mock_get_health.assert_called_once_with(health_id)
        mock_update_health.assert_called_once()
        
        # Verifica o resultado
        assert result.id == mock_health_record.id

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.get_health')
    async def test_update_health_record_not_found(self, mock_get_health, health_update_data):
        """Testa a tentativa de atualizar um registro de saúde inexistente."""
        # Configura o mock para retornar None (registro não encontrado)
        mock_get_health.return_value = None
        
        # Cria o objeto de atualização
        health_update = schemas.HealthUpdate(**health_update_data)
        health_id = uuid4()
        
        # Verifica se a exceção é lançada
        with pytest.raises(HTTPException) as exc_info:
            await services.HealthService.update_health_record(health_id, health_update)
        
        # Verifica o status code e a mensagem de erro
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Registro de saúde não encontrado" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.delete_health')
    @patch('app.modules.health.crud.get_health')
    async def test_delete_health_record_success(
        self, 
        mock_get_health,
        mock_delete_health,
        mock_health_record
    ):
        """Testa a exclusão bem-sucedida de um registro de saúde."""
        # Configura os mocks
        mock_get_health.return_value = mock_health_record
        mock_delete_health.return_value = True
        
        # Chama o método a ser testado
        health_id = uuid4()
        result = await services.HealthService.delete_health_record(health_id)
        
        # Verifica as chamadas aos mocks
        mock_get_health.assert_called_once_with(health_id)
        mock_delete_health.assert_called_once_with(health_id)
        
        # Verifica o resultado
        assert result is True

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.get_health')
    async def test_delete_health_record_not_found(self, mock_get_health):
        """Testa a tentativa de excluir um registro de saúde inexistente."""
        # Configura o mock para retornar None (registro não encontrado)
        mock_get_health.return_value = None
        
        # Verifica se a exceção é lançada
        health_id = uuid4()
        with pytest.raises(HTTPException) as exc_info:
            await services.HealthService.delete_health_record(health_id)
        
        # Verifica o status code e a mensagem de erro
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Registro de saúde não encontrado" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.modules.health.crud.get_health_by_cidadao')
    @patch('app.modules.citizenship.crud.get_cidadao')
    async def test_get_citizen_health_records_success(
        self,
        mock_get_cidadao,
        mock_get_health_by_cidadao,
        mock_cidadao,
        mock_health_record
    ):
        """Testa a busca bem-sucedida dos registros de saúde de um cidadão."""
        # Configura os mocks
        mock_get_cidadao.return_value = mock_cidadao
        mock_get_health_by_cidadao.return_value = [mock_health_record]
        
        # Chama o método a ser testado
        cidadao_id = uuid4()
        result = await services.HealthService.get_citizen_health_records(cidadao_id)
        
        # Verifica as chamadas aos mocks
        mock_get_cidadao.assert_called_once_with(cidadao_id)
        mock_get_health_by_cidadao.assert_called_once_with(
            cidadao_id=cidadao_id,
            skip=0,
            limit=100
        )
        
        # Verifica o resultado
        assert len(result) == 1
        assert result[0].id == mock_health_record.id

    @pytest.mark.asyncio
    @patch('app.modules.citizenship.crud.get_cidadao')
    async def test_get_citizen_health_records_citizen_not_found(self, mock_get_cidadao):
        """Testa a busca de registros para um cidadão inexistente."""
        # Configura o mock para retornar None (cidadão não encontrado)
        mock_get_cidadao.return_value = None
        
        # Verifica se a exceção é lançada
        cidadao_id = uuid4()
        with pytest.raises(HTTPException) as exc_info:
            await services.HealthService.get_citizen_health_records(cidadao_id)
        
        # Verifica o status code e a mensagem de erro
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Cidadão não encontrado" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_recent_health_metrics(self):
        """Testa a geração de métricas de saúde recentes."""
        # Chama o método a ser testado
        days = 30
        result = await services.HealthService.get_recent_health_metrics(days)
        
        # Verifica a estrutura do resultado
        assert "period" in result
        assert "start" in result["period"]
        assert "end" in result["period"]
        assert "total_consultas" in result
        assert "consultas_por_tipo" in result
        assert "media_consultas_por_dia" in result
        assert "diagnosticos_comuns" in result

