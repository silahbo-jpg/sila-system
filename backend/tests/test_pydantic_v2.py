"""Test Pydantic V2 compatibility."""
import pytest
from datetime import date
from app.modules.citizenship.schemas.atualizacao_b_i import AtualizacaoBIBase
from app.modules.citizenship.schemas.emissao_b_i import EmissaoBIBase
from app.modules.citizenship.schemas.emissao_passaporte import EmissaoPassaporteBase

def test_atualizacao_bi_schema():
    """Test AtualizacaoBIBase schema compatibility with Pydantic V2."""
    data = {
        "nome_completo": "Test User",
        "nome_pai": "Father Name",
        "nome_mae": "Mother Name",
        "data_nascimento": "2000-01-01",
        "local_nascimento": "Test Location",
        "estado_civil": "Solteiro",
        "genero": "M",
        "altura": "1.75",
        "residencia": "Test Address",
        "distrito": "Test District",
        "posto_administrativo": "Test Post",
        "localidade": "Test Locality",
        "bairro": "Test Neighborhood",
        "telefone": "123456789",
        "email": "test@example.com",
        "documento_identificacao": "123456789LA123",
        "comprovativo_residencia": "residence_proof.pdf",
        "fotografia": "photo.jpg"
    }
    
    # This will raise an exception if there are any Pydantic V2 compatibility issues
    model = AtualizacaoBIBase(**data)
    assert model.nome_completo == "Test User"
    assert model.data_nascimento == date(2000, 1, 1)

def test_emissao_bi_schema():
    """Test EmissaoBIBase schema compatibility with Pydantic V2."""
    data = {
        "nome_completo": "Test User",
        "nome_pai": "Father Name",
        "nome_mae": "Mother Name",
        "data_nascimento": "2000-01-01",
        "local_nascimento": "Test Location",
        "estado_civil": "Solteiro",
        "genero": "M",
        "altura": "1.75",
        "residencia": "Test Address",
        "distrito": "Test District",
        "posto_administrativo": "Test Post",
        "localidade": "Test Locality",
        "bairro": "Test Neighborhood",
        "telefone": "123456789",
        "email": "test@example.com",
        "documento_identificacao": "123456789LA123",
        "comprovativo_residencia": "residence_proof.pdf",
        "fotografia": "photo.jpg"
    }
    
    # This will raise an exception if there are any Pydantic V2 compatibility issues
    model = EmissaoBIBase(**data)
    assert model.nome_completo == "Test User"
    assert model.data_nascimento == date(2000, 1, 1)

def test_emissao_passaporte_schema():
    """Test EmissaoPassaporteBase schema compatibility with Pydantic V2."""
    data = {
        "numero_bi": "123456789LA123",
        "nome_completo": "Test User",
        "data_nascimento": "2000-01-01",
        "local_nascimento": "Test Location",
        "nome_pai": "Father Name",
        "nome_mae": "Mother Name",
        "estado_civil": "Solteiro",
        "genero": "M",
        "altura": "1.75",
        "residencia": "Test Address",
        "telefone": "123456789",
        "email": "test@example.com",
        "motivo_viagem": "Turismo",
        "pais_destino": "Portugal",
        "data_prevista_viagem": "2023-12-31",
        "documento_identificacao": "123456789LA123",
        "comprovativo_residencia": "residence_proof.pdf",
        "fotografia": "photo.jpg"
    }
    
    # This will raise an exception if there are any Pydantic V2 compatibility issues
    model = EmissaoPassaporteBase(**data)
    assert model.nome_completo == "Test User"
    assert model.data_nascimento == date(2000, 1, 1)
