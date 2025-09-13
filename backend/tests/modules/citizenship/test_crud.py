"""Testes para a camada CRUD do módulo de cidadania."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date, datetime, timedelta
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.modules.citizenship import crud, schemas, models
from app.core.exceptions import ValidationException, NotFoundException

# Fixtures

@pytest.fixture
def mock_db_session():
    """Cria uma sessão mock do banco de dados assíncrona."""
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def cidadao_crud(mock_db_session):
    """Cria uma instância do CidadaoCRUD para testes."""
    return crud.CidadaoCRUD(mock_db_session)

@pytest.fixture
def sample_cidadao_data():
    """Retorna dados de exemplo para criação de um cidadão."""
    return {
        "bi_numero": "123456789LA123",
        "nome_completo": "João da Silva",
        "data_nascimento": date(1990, 1, 1),
        "genero": "M",
        "estado_civil": "solteiro",
        "naturalidade": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna": "Maianga",
        "bairro": "Alvalade",
        "provincia": "Luanda",
        "telefone_principal": "+244923456789",
        "telefone_secundario": "+244912345678",
        "email": "joao.silva@example.com"
    }

@pytest.fixture
def sample_cidadao_model(sample_cidadao_data):
    """Cria um modelo de cidadão de exemplo."""
    cidadao_id = uuid.uuid4()
    return models.Citizen(
        id=cidadao_id,
        **sample_cidadao_data,
        data_registro=datetime.utcnow(),
        ultima_atualizacao=datetime.utcnow(),
        status="ATIVO"
    )

# Testes para CidadaoCRUD

class TestCidadaoCRUD:
    """Testes para a classe CidadaoCRUD."""
    
    @pytest.mark.asyncio
    async def test_criar_cidadao_success(self, cidadao_crud, mock_db_session, sample_cidadao_data):
        """Testa a criação bem-sucedida de um cidadão."""
        # Configura o mock para retornar None (nenhum cidadão com o mesmo BI)
        cidadao_crud.get_by_bi = AsyncMock(return_value=None)
        
        # Cria um mock para o objeto retornado pelo create
        mock_cidadao = MagicMock()
        cidadao_crud.create = AsyncMock(return_value=mock_cidadao)
        
        # Cria um mock para o método de auditoria
        cidadao_crud._criar_log_auditoria = AsyncMock()
        
        # Executa o método
        cidadao_data = schemas.CidadaoCreate(**sample_cidadao_data)
        result = await cidadao_crud.criar_cidadao(cidadao_data)
        
        # Verifica os resultados
        assert result == mock_cidadao
        cidadao_crud.get_by_bi.assert_awaited_once_with(sample_cidadao_data["bi_numero"])
        cidadao_crud.create.assert_awaited_once()
        cidadao_crud._criar_log_auditoria.assert_awaited_once()
        mock_db_session.commit.assert_awaited_once()
        mock_db_session.refresh.assert_awaited_once_with(mock_cidadao)
    
    @pytest.mark.asyncio
    async def test_criar_cidadao_bi_duplicado(self, cidadao_crud, sample_cidadao_data):
        """Testa a tentativa de criar um cidadão com BI duplicado."""
        # Configura o mock para retornar um cidadão existente (BI duplicado)
        cidadao_crud.get_by_bi = AsyncMock(return_value=MagicMock())
        
        # Executa o método e verifica a exceção
        cidadao_data = schemas.CidadaoCreate(**sample_cidadao_data)
        
        with pytest.raises(ValidationException) as exc_info:
            await cidadao_crud.criar_cidadao(cidadao_data)
        
        # Verifica a mensagem de erro
        assert "já cadastrado" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_criar_cidadao_telefone_invalido(self, cidadao_crud, sample_cidadao_data):
        """Testa a validação de telefone inválido."""
        # Configura dados com telefone inválido
        sample_cidadao_data["telefone_principal"] = "12345"
        cidadao_data = schemas.CidadaoCreate(**sample_cidadao_data)
        
        # Executa o método e verifica a exceção
        with pytest.raises(ValidationException) as exc_info:
            await cidadao_crud.criar_cidadao(cidadao_data)
        
        # Verifica a mensagem de erro
        assert "telefone" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_buscar_cidadao_por_id_encontrado(self, cidadao_crud, sample_cidadao_model):
        """Testa a busca de um cidadão por ID (encontrado)."""
        # Configura o mock para retornar o cidadão
        cidadao_id = sample_cidadao_model.id
        cidadao_crud.get = AsyncMock(return_value=sample_cidadao_model)
        
        # Executa o método
        result = await cidadao_crud.get(cidadao_crud.db, cidadao_id)
        
        # Verifica os resultados
        assert result == sample_cidadao_model
        cidadao_crud.get.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_buscar_cidadao_por_id_nao_encontrado(self, cidadao_crud):
        """Testa a busca de um cidadão por ID (não encontrado)."""
        # Configura o mock para retornar None (não encontrado)
        cidadao_id = uuid.uuid4()
        cidadao_crud.get = AsyncMock(return_value=None)
        
        # Executa o método e verifica a exceção
        with pytest.raises(NotFoundException):
            await cidadao_crud.get(cidadao_crud.db, cidadao_id)
        
        # Verifica a chamada
        cidadao_crud.get.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_atualizar_cidadao_sucesso(self, cidadao_crud, sample_cidadao_model):
        """Testa a atualização bem-sucedida de um cidadão."""
        # Dados de atualização
        update_data = {"telefone_principal": "+244923333333"}
        
        # Configura o mock
        cidadao_crud.get = AsyncMock(return_value=sample_cidadao_model)
        cidadao_crud.update = AsyncMock(return_value=sample_cidadao_model)
        
        # Executa o método
        result = await cidadao_crud.update(cidadao_crud.db, sample_cidadao_model.id, update_data)
        
        # Verifica os resultados
        assert result == sample_cidadao_model
        cidadao_crud.get.assert_awaited_once()
        cidadao_crud.update.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_remover_cidadao_sucesso(self, cidadao_crud, sample_cidadao_model):
        """Testa a remoção bem-sucedida de um cidadão."""
        # Configura o mock
        cidadao_crud.get = AsyncMock(return_value=sample_cidadao_model)
        cidadao_crud.remove = AsyncMock()
        
        # Executa o método
        await cidadao_crud.remove(cidadao_crud.db, sample_cidadao_model.id)
        
        # Verifica as chamadas
        cidadao_crud.get.assert_awaited_once()
        cidadao_crud.remove.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_listar_cidadaos_com_filtros(self, cidadao_crud):
        """Testa a listagem de cidadãos com filtros."""
        # Dados de teste
        mock_cidadaos = [MagicMock(), MagicMock()]
        total = 2
        
        # Configura o mock
        cidadao_crud.get_multi = AsyncMock(return_value=(mock_cidadaos, total))
        
        # Executa o método
        result, result_total = await cidadao_crud.buscar_cidadaos_paginados(
            page=1,
            per_page=10,
            nome="João",
            municipio="Luanda",
            status="ATIVO"
        )
        
        # Verifica os resultados
        assert result == mock_cidadaos
        assert result_total == total
        cidadao_crud.get_multi.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_validar_telefone_valido(self, cidadao_crud):
        """Testa a validação de telefone válido."""
        # Telefones válidos
        validos = [
            "+244923456789",
            "+244912345678",
            "+244912345678"
        ]
        
        for telefone in validos:
            # Não deve levantar exceção
            cidadao_crud._validar_telefone(telefone)
    
    @pytest.mark.asyncio
    async def test_validar_telefone_invalido(self, cidadao_crud):
        """Testa a validação de telefone inválido."""
        # Telefones inválidos
        invalidos = [
            "12345",
            "+244123",
            "+2449123456789012345",
            "abc123",
            ""
        ]
        
        for telefone in invalidos:
            with pytest.raises(ValidationException):
                cidadao_crud._validar_telefone(telefone)
    
    @pytest.mark.asyncio
    async def test_validar_email_valido(self, cidadao_crud):
        """Testa a validação de email válido."""
        # Emails válidos
        validos = [
            "usuario@exemplo.com",
            "usuario.nome@exemplo.co.ao",
            "usuario+tag@exemplo.ao"
        ]
        
        for email in validos:
            # Não deve levantar exceção
            cidadao_crud._validar_email(email)
    
    @pytest.mark.asyncio
    async def test_validar_email_invalido(self, cidadao_crud):
        """Testa a validação de email inválido."""
        # Emails inválidos
        invalidos = [
            "semarroba",
            "semdominio@",
            "@semusuario.com",
            "invalido@.com",
            "espaço@exemplo.com"
        ]
        
        for email in invalidos:
            with pytest.raises(ValidationException):
                cidadao_crud._validar_email(email)

