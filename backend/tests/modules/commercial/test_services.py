"""Testes para os serviços do módulo commercial."""
import pytest
import io
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.commercial import services, schemas, models
from app.auth.models import postgres


class TestCommercialServices:
    """Testes para os serviços do módulo commercial."""
    
    @pytest.fixture
    def db_session(self):
        """Cria uma sessão de banco de dados mockada."""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def current_user(self):
        """Cria um usuário de teste."""
        postgres = postgres(
            id=1,
            username="testuser",
            email="test@example.com",
            is_active=True
        )
        return postgres
    
    @pytest.fixture
    def license_data(self):
        """Dados de exemplo para uma licença comercial."""
        return schemas.CommercialLicenseCreate(
            nif="123456789AA123",
            nome_empresa="Empresa Teste",
            categoria=schemas.CategoriaComercial.AMBULANTE,
            atividade="Venda de produtos",
            provincia="Luanda",
            municipio="Belas",
            bairro="Talatona",
            endereco="Rua das Flores, 123"
        )
    
    @pytest.fixture
    def active_license(self):
        """Cria uma licença ativa de exemplo."""
        return models.CommercialLicense(
            id=1,
            nif="123456789AA123",
            nome_empresa="Empresa Existente",
            categoria=schemas.CategoriaComercial.AMBULANTE,
            estado=schemas.EstadoLicenca.ATIVA,
            data_emissao=datetime.utcnow() - timedelta(days=30),
            data_validade=datetime.utcnow() + timedelta(days=335)
        )
    
    @pytest.mark.asyncio
    async def test_create_license_unique_ambulante_rule(
        self, db_session, current_user, license_data, active_license
    ):
        """Testa a regra de negócio que limita uma licença ativa por NIF na categoria ambulante."""
        # Configura o mock do CRUD para retornar uma licença ativa existente
        mock_crud = AsyncMock()
        mock_crud.get_by_nif.return_value = [active_license]
        
        # Cria o serviço com o mock do CRUD
        service = services.CommercialLicenseService(mock_crud)
        
        # Tenta criar uma nova licença para o mesmo NIF na categoria ambulante
        with pytest.raises(HTTPException) as exc_info:
            await service.create_license(license_data, current_user)
        
        # Verifica se a exceção foi lançada com o status e mensagem corretos
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Já existe uma licença ativa para este NIF na categoria AMBULANTE" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_create_license_different_category_allowed(
        self, db_session, current_user, license_data, active_license
    ):
        """Testa que é permitido ter licenças em categorias diferentes para o mesmo NIF."""
        # Muda a categoria da licença existente para uma categoria diferente
        active_license.categoria = schemas.CategoriaComercial.COMERCIO_FIXO
        
        # Configura o mock do CRUD
        mock_crud = AsyncMock()
        mock_crud.get_by_nif.return_value = [active_license]
        mock_crud.create.return_value = models.CommercialLicense(
            id=2,
            nif=license_data.nif,
            nome_empresa=license_data.nome_empresa,
            categoria=license_data.categoria,
            estado=schemas.EstadoLicenca.PENDENTE,
            data_emissao=datetime.utcnow(),
            data_validade=datetime.utcnow() + timedelta(days=365)
        )
        
        # Cria o serviço com o mock do CRUD
        service = services.CommercialLicenseService(mock_crud)
        
        # Tenta criar uma nova licença para o mesmo NIF, mas em categoria diferente
        result = await service.create_license(license_data, current_user)
        
        # Verifica se a licença foi criada com sucesso
        assert result is not None
        assert result.categoria == schemas.CategoriaComercial.AMBULANTE
        assert result.estado == schemas.EstadoLicenca.PENDENTE

    @pytest.mark.asyncio
    async def test_gerar_pdf_com_qrcode(self, mock_licenca):
        """Testa a geração de PDF com QR Code."""
        # Chama a função que será testada
        response = services.gerar_pdf_com_qrcode(mock_licenca)
        
        # Verifica se a resposta é do tipo StreamingResponse
        assert response.__class__.__name__ == "StreamingResponse"
        
        # Verifica o tipo de mídia da resposta
        assert response.media_type == "application/pdf"
        
        # Verifica se o conteúdo do PDF pode ser lido
        content = b"".join([chunk async for chunk in response.body_iterator])
        assert len(content) > 0
        
        # Verifica se o conteúdo parece ser um PDF (verifica o cabeçalho do PDF)
        assert content.startswith(b'%PDF')

    @pytest.mark.asyncio
    async def test_gerar_pdf_com_qrcode_invalid_data(self):
        """Testa a geração de PDF com dados inválidos."""
        # Cria um mock de licença com dados inválidos
        mock_licenca = MagicMock()
        mock_licenca.id = 1
        
        # Remove atributos necessários para forçar um erro
        del mock_licenca.nomeEmpresa
        
        # Verifica se uma exceção é lançada
        with pytest.raises(AttributeError):
            services.gerar_pdf_com_qrcode(mock_licenca)

