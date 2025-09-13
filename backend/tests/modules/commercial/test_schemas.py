"""Testes para os schemas do módulo commercial."""
import pytest
from datetime import datetime, timedelta

from app.modules.commercial import schemas


def test_licenca_create_valid():
    """Testa a criação de um schema de licença com dados válidos."""
    data = {
        "nomeEmpresa": "Empresa Teste Ltda",
        "nif": "123456789",
        "atividade": "Comércio de Produtos",
        "endereco": "Rua Teste, 123",
        "validade": (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%d"),
        "estado": "ativo"
    }
    
    licenca = schemas.LicencaCreate(**data)
    
    assert licenca.nome_empresa == data["nomeEmpresa"]
    assert licenca.nif == data["nif"]
    assert licenca.atividade == data["atividade"]
    assert licenca.endereco == data["endereco"]
    assert licenca.validade == data["validade"]
    assert licenca.estado == data["estado"]


def test_licenca_response_valid():
    """Testa a criação de um schema de resposta de licença com dados válidos."""
    data = {
        "id": 1,
        "nomeEmpresa": "Empresa Teste Ltda",
        "nif": "123456789",
        "atividade": "Comércio de Produtos",
        "endereco": "Rua Teste, 123",
        "validade": (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%d"),
        "estado": "ativo",
        "userId": 1,
        "criadoEm": datetime.utcnow()
    }
    
    licenca = schemas.LicencaResponse(**data)
    
    assert licenca.id == data["id"]
    assert licenca.user_id == data["userId"]
    assert licenca.criado_em == data["criadoEm"]


def test_licenca_create_default_estado():
    """Testa se o estado padrão é definido corretamente."""
    data = {
        "nomeEmpresa": "Empresa Teste Ltda",
        "nif": "123456789",
        "atividade": "Comércio de Produtos",
        "endereco": "Rua Teste, 123",
        "validade": (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%d")
    }
    
    licenca = schemas.LicencaCreate(**data)
    
    assert licenca.estado == "ativo"  # Valor padrão esperado

