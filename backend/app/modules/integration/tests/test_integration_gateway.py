import pytest
import asyncio
from unittest.mock import MagicMock, patch
from datetime import datetime
import json

from sqlalchemy.orm import Session
from app.modules.integration.integration_gateway import IntegrationGateway, integration_gateway
from app.modules.integration.models import IntegrationEvent

@pytest.fixture
def mock_db():
    """Fixture para simular o banco de dados."""
    db = MagicMock(spec=Session)
    
    # Simular o comportamento do add, commit e refresh
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()
    db.query = MagicMock()
    
    return db

@pytest.fixture
def reset_gateway():
    """Fixture para resetar o estado do gateway entre testes."""
    # Resetar o singleton para cada teste
    IntegrationGateway._instance = None
    IntegrationGateway._subscriptions = {}
    IntegrationGateway._initialized = False
    
    yield
    
    # Limpar após o teste
    IntegrationGateway._instance = None
    IntegrationGateway._subscriptions = {}
    IntegrationGateway._initialized = False

def test_singleton_pattern(reset_gateway):
    """Testa se o IntegrationGateway implementa o padrão Singleton."""
    gateway1 = IntegrationGateway()
    gateway2 = IntegrationGateway()
    
    assert gateway1 is gateway2
    assert id(gateway1) == id(gateway2)

def test_subscribe_and_unsubscribe(reset_gateway):
    """Testa a inscrição e cancelamento de inscrição em eventos."""
    gateway = IntegrationGateway()
    callback = MagicMock()
    
    # Testar inscrição
    gateway.subscribe("test_module", "test.event", callback)
    assert "test.event" in gateway._subscriptions
    assert len(gateway._subscriptions["test.event"]) == 1
    assert gateway._subscriptions["test.event"][0].module == "test_module"
    assert gateway._subscriptions["test.event"][0].callback == callback
    
    # Testar cancelamento de inscrição
    gateway.unsubscribe("test_module", "test.event")
    assert len(gateway._subscriptions["test.event"]) == 0

@pytest.mark.asyncio
async def test_publish_event(reset_gateway, mock_db):
    """Testa a publicação de eventos."""
    gateway = IntegrationGateway()
    
    # Configurar o mock para simular a criação do evento
    event = IntegrationEvent(
        id=1,
        event_type="test.event",
        payload=json.dumps({"test": "data"}),
        source_module="test_module",
        timestamp=datetime.now()
    )
    
    # Simular o comportamento do refresh para definir o ID
    def side_effect(obj):
        obj.id = 1
    mock_db.refresh.side_effect = side_effect
    
    # Testar publicação de evento
    with patch.object(gateway, '_notify_subscribers', return_value=asyncio.Future()) as mock_notify:
        mock_notify.return_value.set_result(None)
        
        result = await gateway.publish(
            event_type="test.event",
            payload={"test": "data"},
            source_module="test_module",
            db=mock_db
        )
        
        # Verificar se o evento foi criado e persistido
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called
        
        # Verificar se a nnnnnnnotificação foi chamada
        assert mock_notify.called

@pytest.mark.asyncio
async def test_notify_subscribers(reset_gateway):
    """Testa a nnnnnnnotificação de assinantes quando um evento é publicado."""
    gateway = IntegrationGateway()
    
    # Criar callbacks mock
    callback1 = MagicMock()
    callback2 = MagicMock()
    
    # Registrar assinantes
    gateway.subscribe("module1", "test.event", callback1)
    gateway.subscribe("module2", "test.event", callback2, {"key": "value"})
    
    # Criar evento de teste
    event = IntegrationEvent(
        id=1,
        event_type="test.event",
        payload=json.dumps({"test": "data", "key": "value"}),
        source_module="test_module",
        timestamp=datetime.now()
    )
    
    # Testar nnnnnnnotificação
    with patch.object(gateway, '_safe_callback', return_value=asyncio.Future()) as mock_safe_callback:
        mock_safe_callback.return_value.set_result(None)
        
        await gateway._notify_subscribers(
            event_type="test.event",
            event=event,
            payload={"test": "data", "key": "value"}
        )
        
        # Verificar se os callbacks foram chamados
        assert mock_safe_callback.call_count == 2

@pytest.mark.asyncio
async def test_safe_callback_sync(reset_gateway):
    """Testa a execução segura de callbacks síncronos."""
    gateway = IntegrationGateway()
    
    # Criar callback mock
    callback = MagicMock()
    
    # Criar evento de teste
    event = IntegrationEvent(
        id=1,
        event_type="test.event",
        payload=json.dumps({"test": "data"}),
        source_module="test_module",
        timestamp=datetime.now()
    )
    
    # Testar execução segura
    await gateway._safe_callback(
        callback=callback,
        event=event,
        payload={"test": "data"},
        module="test_module"
    )
    
    # Verificar se o callback foi chamado
    callback.assert_called_once_with(event, {"test": "data"})

@pytest.mark.asyncio
async def test_safe_callback_async(reset_gateway):
    """Testa a execução segura de callbacks assíncronos."""
    gateway = IntegrationGateway()
    
    # Criar callback assíncrono mock
    async def async_callback(event, payload):
        return True
    
    async_mock = MagicMock()
    async_mock.side_effect = async_callback
    
    # Criar evento de teste
    event = IntegrationEvent(
        id=1,
        event_type="test.event",
        payload=json.dumps({"test": "data"}),
        source_module="test_module",
        timestamp=datetime.now()
    )
    
    # Testar execução segura
    with patch('asyncio.iscoroutinefunction', return_value=True):
        await gateway._safe_callback(
            callback=async_mock,
            event=event,
            payload={"test": "data"},
            module="test_module"
        )
        
        # Verificar se o callback foi chamado
        async_mock.assert_called_once_with(event, {"test": "data"})

@pytest.mark.asyncio
async def test_safe_callback_exception(reset_gateway):
    """Testa o tratamento de exceções em callbacks."""
    gateway = IntegrationGateway()
    
    # Criar callback que lança exceção
    callback = MagicMock(side_effect=Exception("Test exception"))
    
    # Criar evento de teste
    event = IntegrationEvent(
        id=1,
        event_type="test.event",
        payload=json.dumps({"test": "data"}),
        source_module="test_module",
        timestamp=datetime.now()
    )
    
    # Testar tratamento de exceção
    with patch('logging.getLogger') as mock_logger:
        mock_logger.return_value.error = MagicMock()
        
        # Não deve lançar exceção
        await gateway._safe_callback(
            callback=callback,
            event=event,
            payload={"test": "data"},
            module="test_module"
        )
        
        # Verificar se o erro foi registrado
        assert mock_logger.return_value.error.called

