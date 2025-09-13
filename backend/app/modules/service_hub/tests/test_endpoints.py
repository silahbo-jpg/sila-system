# Tests for Service Hub endpoints

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.modules.service_hub import models, schemas, crud, services


@pytest.fixture
def client():
    """Fixture para o cliente de teste."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Fixture para cabeçalhos de autenticação (mock)."""
    # Em um teste real, você obteria um token JWT válido
    return {"Authorization": "Bearer test_token"}


@pytest.fixture
def admin_auth_headers():
    """Fixture para cabeçalhos de autenticação de administrador (mock)."""
    # Em um teste real, você obteria um token JWT válido para um administrador
    return {"Authorization": "Bearer admin_test_token"}


@pytest.fixture
def sample_service(db: Session):
    """Fixture para criar um serviço de teste."""
    service_data = {
        "slug": "test-api-service",
        "nome": "Serviço de Teste API",
        "descricao": "Um serviço para testes de API",
        "departamento": "testes",
        "categoria": "testes",
        "sla_horas": 24,
        "requer_autenticacao": True,
        "requer_documentos": ["documento_teste"],
        "eventos": ["teste_iniciado", "teste_concluido"]
    }
    
    service_schema = schemas.ServicoCreate(**service_data)
    service = crud.create_servico(db=db, servico=service_schema)
    
    yield service
    
    # Limpar o banco de dados
    db.delete(service)
    db.commit()


def test_get_available_services(client, sample_service):
    """Testa a obtenção de serviços disponíveis."""
    response = client.get("/service_hub/available")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Verificar se o serviço de teste está na lista
    service_ids = [service["id"] for service in response.json()]
    assert sample_service.id in service_ids


def test_get_service_by_slug(client, sample_service):
    """Testa a obtenção de um serviço pelo slug."""
    response = client.get(f"/service_hub/services/{sample_service.slug}")
    
    assert response.status_code == 200
    assert response.json()["id"] == sample_service.id
    assert response.json()["nome"] == sample_service.nome


def test_create_service(client, admin_auth_headers, db: Session):
    """Testa a criação de um serviço."""
    service_data = {
        "slug": "new-test-service",
        "nome": "Novo Serviço de Teste",
        "descricao": "Um novo serviço para testes",
        "departamento": "testes",
        "categoria": "testes",
        "sla_horas": 48,
        "requer_autenticacao": True,
        "requer_documentos": ["documento_novo"],
        "eventos": ["novo_teste_iniciado", "novo_teste_concluido"]
    }
    
    response = client.post(
        "/service_hub/services",
        json=service_data,
        headers=admin_auth_headers
    )
    
    assert response.status_code == 201
    assert response.json()["slug"] == service_data["slug"]
    assert response.json()["nome"] == service_data["nome"]
    
    # Limpar o banco de dados
    service_id = response.json()["id"]
    service = crud.get_servico(db=db, servico_id=service_id)
    if service:
        db.delete(service)
        db.commit()


def test_update_service(client, admin_auth_headers, sample_service):
    """Testa a atualização de um serviço."""
    update_data = {
        "nome": "Serviço de Teste Atualizado",
        "sla_horas": 36
    }
    
    response = client.put(
        f"/service_hub/services/{sample_service.id}",
        json=update_data,
        headers=admin_auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["nome"] == update_data["nome"]
    assert response.json()["sla_horas"] == update_data["sla_horas"]


def test_create_service_request(client, auth_headers, sample_service):
    """Testa a criação de uma solicitação de serviço."""
    request_data = {
        "servico_id": sample_service.id,
        "cidadao_id": 1,  # Assumindo que existe um cidadão com ID 1
        "dados_solicitacao": {"campo_teste": "valor_teste"},
        "documentos_anexados": ["doc_teste.pdf"],
        "observacoes": "Solicitação de teste via API"
    }
    
    response = client.post(
        "/service_hub/requests",
        json=request_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    assert response.json()["servico_id"] == request_data["servico_id"]
    assert response.json()["cidadao_id"] == request_data["cidadao_id"]
    assert response.json()["status"] == "pendente"

