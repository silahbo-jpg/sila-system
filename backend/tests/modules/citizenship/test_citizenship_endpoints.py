"""
Testes para os endpoints do módulo de cidadania.
"""
import pytest
from fastapi import status
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

# Test data
TEST_CITIZEN = {
    "nome_completo": "João da Silva",
    "numero_bi": "123456789LA041",
    "cpf": "12345678901",
    "data_nascimento": "1990-01-01",
    "genero": "M",
    "estado_civil": "SOLTEIRO",
    "nome_mae": "Maria da Silva",
    "nome_pai": "José da Silva",
    "naturalidade": "Luanda",
    "nacionalidade": "Angolana",
    "morada": "Rua dos Testes, 123",
    "bairro": "Centro",
    "municipio": "Luanda",
    "provincia": "Luanda",
    "telefone": "912345678",
    "email": "joao.silva@example.com"
}

TEST_ATESTADO = {
    "tipo": "RESIDENCIA",
    "descricao": "Atestado de residência para fins de documentação",
    "cidadania_id": 1
}

def setup_mocks(mock_client):
    """Configura os mocks para simular o banco de dados."""
    # Mock para get_current_user
    from app.auth.security import get_current_user
    # Fixing the import - using the correct Prisma models
    from prisma.models import User
    
    # Cria um usuário de teste
    test_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=True
    )
    
    # Mock para get_current_user
    async def mock_get_current_user():
        return test_user
    
    # Aplica o mock
    import app.main
    app.main.get_current_user = mock_get_current_user
    
    # Mock para operações de cidadão
    mock_citizen = MagicMock()
    mock_citizen.id = 1
    mock_citizen.nome_completo = "Teste da Silva"
    mock_citizen.numero_bi = "123456789LA123"
    mock_citizen.cpf = "12345678901"
    mock_citizen.data_nascimento = datetime(1990, 1, 1).date()
    mock_citizen.genero = "M"
    mock_citizen.estado_civil = "SOLTEIRO"
    mock_citizen.nome_mae = "Mãe do Teste"
    mock_citizen.nome_pai = "Pai do Teste"
    mock_citizen.naturalidade = "Testelândia"
    mock_citizen.nacionalidade = "Brasileiro"
    mock_citizen.morada = "Rua dos Testes, 123"
    mock_citizen.bairro = "Centro"
    mock_citizen.municipio = "Testelândia"
    mock_citizen.provincia = "Teste"
    mock_citizen.telefone = "912345678"
    mock_citizen.email = "teste@example.com"
    
    # Configura os mocks para as operações do banco de dados
    mock_client.citizen = AsyncMock()
    mock_client.citizen.find_unique.return_value = mock_citizen
    mock_client.citizen.find_many.return_value = [mock_citizen]
    mock_client.citizen.create.return_value = mock_citizen
    mock_client.citizen.update.return_value = mock_citizen
    mock_client.citizen.delete.return_value = mock_citizen
    
    # Mock para operações de atestado
    mock_atestado = MagicMock()
    mock_atestado.id = 1
    mock_atestado.tipo = "RESIDENCIA"
    mock_atestado.descricao = "Atestado de residência para fins de documentação"
    mock_atestado.cidadania_id = 1
    mock_atestado.user_id = 1
    mock_atestado.data_emissao = datetime.now()
    
    mock_client.atestado = AsyncMock()
    mock_client.atestado.find_unique.return_value = mock_atestado
    mock_client.atestado.find_many.return_value = [mock_atestado]
    mock_client.atestado.create.return_value = mock_atestado


def test_list_citizens(client):
    """Testa a listagem de cidadãos."""
    response = client.get("/api/citizenship/citizens/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["nome_completo"] == "Teste da Silva"


def test_get_citizen(client):
    """Testa a obtenção de um cidadão específico."""
    response = client.get("/api/citizenship/citizens/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome_completo"] == "Teste da Silva"
    assert data["numero_bi"] == "123456789LA123"


def test_create_citizen(client):
    """Testa a criação de um novo cidadão."""
    response = client.post(
        "/api/citizenship/citizens/",
        json=TEST_CITIZEN
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome_completo"] == TEST_CITIZEN["nome_completo"]
    assert data["numero_bi"] == TEST_CITIZEN["numero_bi"]


def test_update_citizen(client):
    """Testa a atualização de um cidadão existente."""
    update_data = TEST_CITIZEN.copy()
    update_data["nome_completo"] = "Nome Atualizado"
    
    response = client.put(
        "/api/citizenship/citizens/1",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome_completo"] == "Nome Atualizado"


def test_delete_citizen(client):
    """Testa a exclusão de um cidadão."""
    response = client.delete("/api/citizenship/citizens/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_solicitar_atestado(client):
    """Testa a solicitação de um atestado."""
    response = client.post(
        "/api/citizenship/atestados/",
        json=TEST_ATESTADO
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == TEST_ATESTADO["tipo"]
    assert data["descricao"] == TEST_ATESTADO["descricao"]


def test_obter_atestado(client):
    """Testa a obtenção de um atestado específico."""
    response = client.get("/api/citizenship/atestados/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["tipo"] == "RESIDENCIA"
    assert "data_emissao" in data


def test_get_citizenship_summary(client):
    """Testa a obtenção do resumo estatístico."""
    response = client.get("/api/citizenship/reports/summary")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verifica se as chaves esperadas estão presentes
    expected_keys = [
        "total_citizens",
        "gender_distribution",
        "age_distribution",
        "yearly_registrations"
    ]
    
    for key in expected_keys:
        assert key in data, f"Chave '{key}' não encontrada na resposta"
    
    # Verifica se os valores são do tipo esperado
    assert isinstance(data["total_citizens"], int)
    assert isinstance(data["gender_distribution"], dict)
    assert isinstance(data["age_distribution"], dict)
    assert isinstance(data["yearly_registrations"], list)


def test_create_citizen_validation(client):
    """Testa a validação ao criar um cidadão com dados inválidos."""
    invalid_data = TEST_CITIZEN.copy()
    invalid_data["email"] = "email-invalido"  # Email inválido
    
    response = client.post(
        "/api/citizenship/citizens/",
        json=invalid_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Verifica se a mensagem de erro contém informações sobre o campo inválido
    error_data = response.json()
    assert "detail" in error_data
    assert any("email" in str(err).lower() for err in error_data["detail"])


def test_unauthenticated_access(client):
    """Testa o acesso não autenticado a rotas protegidas."""
    # Remove temporariamente o mock de autenticação
    import app.main
    app.main.get_current_user = None
    
    # Tenta acessar uma rota protegida
    response = client.get("/api/citizenship/citizens/")
    
    # Restaura o mock para os próximos testes
    setup_mocks(client.app.state.db)
    
    # Verifica se o acesso foi negado
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_nonexistent_citizen(client):
    """Testa a busca por um cidadão que não existe."""
    # Configura o mock para retornar None (cidadão não encontrado)
    client.app.state.db.citizen.find_unique.return_value = None