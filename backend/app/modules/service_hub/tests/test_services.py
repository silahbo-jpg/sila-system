# Tests for Service Hub services

import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from app.modules.service_hub import models, schemas, crud, services


@pytest.fixture
def sample_service_data():
    """Fixture para dados de exemplo de um serviço."""
    return {
        "slug": "test-service",
        "nome": "Serviço de Teste",
        "descricao": "Um serviço para testes",
        "departamento": "testes",
        "categoria": "testes",
        "sla_horas": 24,
        "requer_autenticacao": True,
        "requer_documentos": ["documento_teste"],
        "eventos": ["teste_iniciado", "teste_concluido"]
    }


def test_register_service(db: Session, sample_service_data):
    """Testa o registro de um novo serviço."""
    # Registrar o serviço
    service = services.ServiceHubService.register_service(db, sample_service_data)
    
    # Verificar se o serviço foi registrado corretamente
    assert service.id is not None
    assert service.slug == sample_service_data["slug"]
    assert service.nome == sample_service_data["nome"]
    assert service.departamento == sample_service_data["departamento"]
    assert service.ativo is True
    
    # Limpar o banco de dados
    db.delete(service)
    db.commit()


def test_get_services_by_department(db: Session, sample_service_data):
    """Testa a obtenção de serviços por departamento."""
    # Registrar o serviço
    service = services.ServiceHubService.register_service(db, sample_service_data)
    
    # Obter serviços do departamento
    department_services = services.ServiceHubService.get_services_by_department(
        db, sample_service_data["departamento"]
    )
    
    # Verificar se o serviço está na lista
    assert len(department_services) > 0
    assert any(s.id == service.id for s in department_services)
    
    # Limpar o banco de dados
    db.delete(service)
    db.commit()


def test_deactivate_service(db: Session, sample_service_data):
    """Testa a desativação de um serviço."""
    # Registrar o serviço
    service = services.ServiceHubService.register_service(db, sample_service_data)
    
    # Desativar o serviço
    updated_service = services.ServiceHubService.deactivate_service(db, service.id)
    
    # Verificar se o serviço foi desativado
    assert updated_service is not None
    assert updated_service.ativo is False
    
    # Limpar o banco de dados
    db.delete(service)
    db.commit()


@pytest.fixture
def sample_request_data(db: Session, sample_service_data):
    """Fixture para dados de exemplo de uma solicitação de serviço."""
    # Criar um serviço para a solicitação
    service = services.ServiceHubService.register_service(db, sample_service_data)
    
    # Dados da solicitação
    request_data = {
        "servico_id": service.id,
        "cidadao_id": 1,  # Assumindo que existe um cidadão com ID 1
        "dados": {"campo_teste": "valor_teste"},
        "documentos": ["doc_teste.pdf"],
        "observacoes": "Solicitação de teste"
    }
    
    yield request_data
    
    # Limpar o banco de dados
    db.delete(service)
    db.commit()


def test_request_service(db: Session, sample_request_data):
    """Testa a criação de uma solicitação de serviço."""
    # Criar a solicitação
    request = services.ServiceRequestService.request_service(
        db=db,
        cidadao_id=sample_request_data["cidadao_id"],
        servico_id=sample_request_data["servico_id"],
        dados=sample_request_data["dados"],
        documentos=sample_request_data["documentos"],
        observacoes=sample_request_data["observacoes"]
    )
    
    # Verificar se a solicitação foi criada corretamente
    assert request.id is not None
    assert request.servico_id == sample_request_data["servico_id"]
    assert request.cidadao_id == sample_request_data["cidadao_id"]
    assert request.status == "pendente"
    
    # Limpar o banco de dados
    db.delete(request)
    db.commit()


def test_update_request_status(db: Session, sample_request_data):
    """Testa a atualização do status de uma solicitação de serviço."""
    # Criar a solicitação
    request = services.ServiceRequestService.request_service(
        db=db,
        cidadao_id=sample_request_data["cidadao_id"],
        servico_id=sample_request_data["servico_id"],
        dados=sample_request_data["dados"],
        documentos=sample_request_data["documentos"],
        observacoes=sample_request_data["observacoes"]
    )
    
    # Atualizar o status da solicitação
    updated_request = services.ServiceRequestService.update_request_status(
        db=db,
        solicitacao_id=request.id,
        status="em_analise",
        observacoes="Em análise pelo departamento"
    )
    
    # Verificar se o status foi atualizado corretamente
    assert updated_request is not None
    assert updated_request.status == "em_analise"
    assert updated_request.observacoes == "Em análise pelo departamento"
    
    # Limpar o banco de dados
    db.delete(request)
    db.commit()

