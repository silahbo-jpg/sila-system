"""Testes para os schemas do módulo de saúde."""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import ValidationError

from app.modules.health import schemas


def test_health_base_validation():
    """Testa a validação básica do schema HealthBase."""
    # Dados válidos
    valid_data = {
        "tipo_consulta": "Consulta de rotina",
        "data_consulta": datetime.utcnow(),
        "cidadao_id": str(uuid4())
    }
    
    # Deve criar o objeto sem erros
    health = schemas.HealthBase(**valid_data)
    assert health.tipo_consulta == valid_data["tipo_consulta"]
    assert health.data_consulta == valid_data["data_consulta"]
    assert str(health.cidadao_id) == valid_data["cidadao_id"]
    
    # Campos opcionais devem ser None por padrão
    assert health.diagnostico is None
    assert health.tratamento is None
    assert health.observacoes is None


def test_health_base_validation_future_date():
    """Testa a validação de data futura no schema HealthBase."""
    # Data futura deve ser rejeitada
    future_date = datetime.utcnow() + timedelta(days=1)
    with pytest.raises(ValueError, match="A data da consulta não pode ser futura"):
        schemas.HealthBase(
            tipo_consulta="Consulta",
            data_consulta=future_date,
            cidadao_id=str(uuid4())
        )


def test_health_create_validation():
    """Testa o schema HealthCreate."""
    # Deve herdar corretamente de HealthBase
    data = {
        "tipo_consulta": "Emergência",
        "data_consulta": datetime.utcnow(),
        "diagnostico": "Hipertensão",
        "tratamento": "Repouso e medicação",
        "observacoes": "Retornar em 7 dias",
        "cidadao_id": str(uuid4())
    }
    
    health = schemas.HealthCreate(**data)
    assert health.dict() == data


def test_health_update_validation():
    """Testa o schema HealthUpdate."""
    # Deve ser possível atualizar campos individuais
    data = {"tipo_consulta": "Retorno"}
    update = schemas.HealthUpdate(**data)
    assert update.dict(exclude_unset=True) == data
    
    # Campos não fornecidos devem ser None
    assert update.data_consulta is None
    assert update.diagnostico is None
    assert update.tratamento is None
    assert update.observacoes is None
    assert update.cidadao_id is None


def test_health_in_db_validation():
    """Testa o schema HealthInDB."""
    now = datetime.utcnow()
    data = {
        "id": 1,
        "created_at": now,
        "updated_at": now,
        "tipo_consulta": "Consulta",
        "data_consulta": now,
        "cidadao_id": str(uuid4())
    }
    
    health = schemas.HealthInDB(**data)
    assert health.id == 1
    assert health.created_at == now
    assert health.updated_at == now

