"""Testes para os schemas Pydantic do módulo de Cidadania."""
import pytest
from datetime import date, datetime, timedelta
from pydantic import ValidationError
from app.modules.citizenship import schemas


# ====================================
# Testes para CidadaoBase e CidadaoCreate
# ====================================

def test_cidadao_base_valid():
    """Testa a criação de um CidadaoBase com dados válidos."""
    data = {
        "bi_numero": "123456789LA123",
        "nome_completo": "João da Silva",
        "data_nascimento": date(1990, 1, 1),
        "genero": schemas.GeneroEnum.MASCULINO,
        "estado_civil": schemas.EstadoCivilEnum.SOLTEIRO,
        "naturalidade": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna": "Maianga",
        "bairro": "Alvalade",
        "provincia": "Luanda",
        "telefone_principal": "+244923456789"
    }
    
    cidadao = schemas.CidadaoBase(**data)
    
    assert cidadao.bi_numero == "123456789LA123"
    assert cidadao.nome_completo == "João da Silva"
    assert cidadao.data_nascimento == date(1990, 1, 1)
    assert cidadao.genero == schemas.GeneroEnum.MASCULINO
    assert cidadao.estado_civil == schemas.EstadoCivilEnum.SOLTEIRO


def test_cidadao_base_invalid_bi():
    """Testa a validação de BI inválido."""
    data = {
        "bi_numero": "123",  # BI muito curto
        "nome_completo": "João da Silva",
        "data_nascimento": date(1990, 1, 1),
        "genero": schemas.GeneroEnum.MASCULINO,
        "estado_civil": schemas.EstadoCivilEnum.SOLTEIRO,
        "naturalidade": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna": "Maianga",
        "bairro": "Alvalade",
        "provincia": "Luanda",
        "telefone_principal": "+244923456789"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schemas.CidadaoBase(**data)
    
    assert "bi_numero" in str(exc_info.value)


def test_cidadao_base_invalid_phone():
    """Testa a validação de telefone inválido."""
    data = {
        "bi_numero": "123456789LA123",
        "nome_completo": "João da Silva",
        "data_nascimento": date(1990, 1, 1),
        "genero": schemas.GeneroEnum.MASCULINO,
        "estado_civil": schemas.EstadoCivilEnum.SOLTEIRO,
        "naturalidade": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna": "Maianga",
        "bairro": "Alvalade",
        "provincia": "Luanda",
        "telefone_principal": "123"  # Telefone inválido
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schemas.CidadaoBase(**data)
    
    assert "telefone_principal" in str(exc_info.value)


def test_cidadao_create_valid():
    """Testa a criação de um CidadaoCreate com dados válidos."""
    data = {
        "bi_numero": "123456789LA123",
        "nome_completo": "Maria dos Santos",
        "data_nascimento": date(1985, 5, 15),
        "genero": schemas.GeneroEnum.FEMININO,
        "estado_civil": schemas.EstadoCivilEnum.CASADO,
        "naturalidade": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna": "Maianga",
        "bairro": "Alvalade",
        "provincia": "Luanda",
        "telefone_principal": "+244923456789",
        "email": "maria@example.com",
        "nome_conjuge": "José dos Santos"
    }
    
    cidadao = schemas.CidadaoCreate(**data)
    
    assert cidadao.email == "maria@example.com"
    assert cidadao.nome_conjuge == "José dos Santos"


def test_cidadao_create_missing_conjuge():
    """Testa a validação de nome do cônjuge para casados."""
    data = {
        "bi_numero": "123456789LA123",
        "nome_completo": "Maria dos Santos",
        "data_nascimento": date(1985, 5, 15),
        "genero": schemas.GeneroEnum.FEMININO,
        "estado_civil": schemas.EstadoCivilEnum.CASADO,  # Estado civil CASADO sem nome do cônjuge
        "naturalidade": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna": "Maianga",
        "bairro": "Alvalade",
        "provincia": "Luanda",
        "telefone_principal": "+244923456789"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schemas.CidadaoCreate(**data)
    
    assert "nome_conjuge" in str(exc_info.value)


# ====================================
# Testes para CidadaoUpdate
# ====================================

def test_cidadao_update_valid():
    """Testa a atualização de um cidadão com dados válidos."""
    data = {
        "telefone_principal": "+244923333333",
        "email": "novo.email@example.com"
    }
    
    update = schemas.CidadaoUpdate(**data)
    
    assert update.telefone_principal == "+244923333333"
    assert update.email == "novo.email@example.com"


def test_cidadao_update_invalid_email():
    """Testa a validação de email inválido na atualização."""
    data = {
        "email": "email-invalido"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schemas.CidadaoUpdate(**data)
    
    assert "email" in str(exc_info.value)


# ====================================
# Testes para Documento e MembroFamiliar
# ====================================

def test_documento_create_valid():
    """Testa a criação de um documento válido."""
    data = {
        "tipo": schemas.TipoDocumentoEnum.RESIDENCIA,
        "data_validade": date(2030, 12, 31)
    }
    
    documento = schemas.DocumentoCreate(**data)
    
    assert documento.tipo == schemas.TipoDocumentoEnum.RESIDENCIA
    assert documento.data_validade == date(2030, 12, 31)


def test_membro_familiar_create_valid():
    """Testa a criação de um membro familiar válido."""
    data = {
        "nome_completo": "Carlos Silva",
        "parentesco": schemas.ParentescoEnum.FILHO,
        "data_nascimento": date(2010, 5, 15),
        "genero": schemas.GeneroEnum.MASCULINO,
        "dependente": True
    }
    
    membro = schemas.MembroFamiliarCreate(**data)
    
    assert membro.nome_completo == "Carlos Silva"
    assert membro.parentesco == schemas.ParentescoEnum.FILHO
    assert membro.dependente is True


# ====================================
# Testes para Feedback
# ====================================

def test_feedback_create_valid():
    """Testa a criação de um feedback válido."""
    data = {
        "tipo": schemas.TipoFeedbackEnum.SUGESTAO,
        "titulo": "Melhoria no atendimento",
        "descricao": "Sugiro ampliar o horário de atendimento.",
        "classificacao": 5
    }
    
    feedback = schemas.FeedbackCreate(**data)
    
    assert feedback.tipo == schemas.TipoFeedbackEnum.SUGESTAO
    assert feedback.titulo == "Melhoria no atendimento"
    assert feedback.classificacao == 5


def test_feedback_invalid_rating():
    """Testa a validação de classificação inválida."""
    data = {
        "tipo": schemas.TipoFeedbackEnum.SUGESTAO,
        "titulo": "Avaliação",
        "descricao": "Teste de classificação inválida.",
        "classificacao": 6  # Valor acima do máximo permitido
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schemas.FeedbackCreate(**data)
    
    assert "classificacao" in str(exc_info.value)


def test_feedback_update_valid():
    """Testa a atualização de um feedback."""
    data = {
        "status": schemas.StatusFeedbackEnum.RESOLVIDO,
        "resposta": "Obrigado pelo seu feedback!"
    }
    
    update = schemas.FeedbackUpdate(**data)
    
    assert update.status == schemas.StatusFeedbackEnum.RESOLVIDO
    assert update.resposta == "Obrigado pelo seu feedback!"


# ====================================
# Testes para funções de validação
# ====================================

def test_validar_telefone_angolano():
    """Testa a validação de números de telefone angolanos."""
    # Formatos válidos
    assert schemas.validar_telefone_angolano("+244923456789") == "+244923456789"
    assert schemas.validar_telefone_angolano("923 456 789") == "+244923456789"
    assert schemas.validar_telefone_angolano("923-456-789") == "+244923456789"
    
    # Número inválido
    with pytest.raises(ValueError):
        schemas.validar_telefone_angolano("123")  # Muito curto


def test_validar_bi():
    """Testa a validação de números de BI angolanos."""
    # Formatos válidos
    assert schemas.validar_bi("123456789LA123") == "123456789LA123"
    assert schemas.validar_bi("123456789la123") == "123456789LA123"  # Converte para maiúsculas
    
    # Número inválido
    with pytest.raises(ValueError):
        schemas.validar_bi("123")  # Muito curto

