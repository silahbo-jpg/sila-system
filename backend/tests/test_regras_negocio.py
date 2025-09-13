"""
Testes para o módulo de regras de negócio.

Este módulo contém testes para as validações e regras de negócio
definidas no módulo core.regras_negocio.
"""
import pytest
from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field

from app.core.regras_negocio import (
    ValidadorDocumentos,
    ValidadorEndereco,
    ValidadorPessoa,
    ValidadorEmpresa,
    ValidadorProcessoJudicial,
    ValidadorNegocio,
    TipoDocumento
)

class TestValidadorDocumentos:
    """Testes para o validador de documentos."""
    
    def test_validar_cpf_valido(self):
        """Testa a validação de CPF válido."""
        assert ValidadorDocumentos.validar_cpf("529.982.247-25") is True
        assert ValidadorDocumentos.validar_cpf("52998224725") is True
    
    def test_validar_cpf_invalido(self):
        """Testa a validação de CPF inválido."""
        assert ValidadorDocumentos.validar_cpf("111.111.111-11") is False  # Dígitos iguais
        assert ValidadorDocumentos.validar_cpf("123.456.789-10") is False  # CPF inválido
        assert ValidadorDocumentos.validar_cpf("") is False  # Vazio
        assert ValidadorDocumentos.validar_cpf("123") is False  # Tamanho inválido
    
    def test_validar_cnpj_valido(self):
        """Testa a validação de CNPJ válido."""
        assert ValidadorDocumentos.validar_cnpj("33.000.167/0001-01") is True  # Receita Federal
        assert ValidadorDocumentos.validar_cnpj("33000167000101") is True
    
    def test_validar_cnpj_invalido(self):
        """Testa a validação de CNPJ inválido."""
        assert ValidadorDocumentos.validar_cnpj("11.111.111/1111-11") is False  # Dígitos iguais
        assert ValidadorDocumentos.validar_cnpj("12.345.678/0001-99") is False  # CNPJ inválido
        assert ValidadorDocumentos.validar_cnpj("") is False  # Vazio
        assert ValidadorDocumentos.validar_cnpj("123") is False  # Tamanho inválido


class TestValidadorEndereco:
    """Testes para o validador de endereços."""
    
    def test_validar_cep_valido(self):
        """Testa a validação de CEP válido."""
        assert ValidadorEndereco.validar_cep("01310-100") is True
        assert ValidadorEndereco.validar_cep("01310100") is True
    
    def test_validar_cep_invalido(self):
        """Testa a validação de CEP inválido."""
        assert ValidadorEndereco.validar_cep("00000000") is False  # Dígitos iguais
        assert ValidadorEndereco.validar_cep("123") is False  # Tamanho inválido
        assert ValidadorEndereco.validar_cep("") is False  # Vazio


class TestValidadorPessoa:
    """Testes para o validador de pessoas."""
    
    def test_validar_data_nascimento_valida(self):
        """Testa a validação de data de nascimento válida."""
        hoje = date.today()
        
        # Data de nascimento válida (18 anos atrás)
        data_valida = hoje.replace(year=hoje.year - 25)
        assert ValidadorPessoa.validar_data_nascimento(data_valida) is True
        
        # Data de nascimento no limite (130 anos atrás)
        data_limite = hoje.replace(year=hoje.year - 130)
        assert ValidadorPessoa.validar_data_nascimento(data_limite) is True
    
    def test_validar_data_nascimento_invalida(self):
        """Testa a validação de data de nascimento inválida."""
        hoje = date.today()
        
        # Data no futuro
        data_futura = hoje.replace(year=hoje.year + 1)
        assert ValidadorPessoa.validar_data_nascimento(data_futura) is False
        
        # Data muito antiga (mais de 130 anos)
        data_muito_antiga = hoje.replace(year=hoje.year - 131)
        assert ValidadorPessoa.validar_data_nascimento(data_muito_antiga) is False
    
    def test_validar_nome_valido(self):
        """Testa a validação de nome válido."""
        assert ValidadorPessoa.validar_nome("João da Silva") is True
        assert ValidadorPessoa.validar_nome("Maria-José D'Ávila") is True
        assert ValidadorPessoa.validar_nome("Antônio dos Santos") is True
    
    def test_validar_nome_invalido(self):
        """Testa a validação de nome inválido."""
        assert ValidadorPessoa.validar_nome("Jo") is False  # Muito curto
        assert ValidadorPessoa.validar_nome("João") is False  # Sem sobrenome
        assert ValidadorPessoa.validar_nome("João 123") is False  # Números
        assert ValidadorPessoa.validar_nome("") is False  # Vazio


class TestValidadorEmpresa:
    """Testes para o validador de empresas."""
    
    def test_validar_ie_sp_valida(self):
        """Testa a validação de Inscrição Estadual de SP válida."""
        # IE de SP válida (exemplo hipotético)
        assert ValidadorEmpresa._validar_ie_sp("110042490114") is True
    
    def test_validar_ie_rj_valida(self):
        """Testa a validação de Inscrição Estadual do RJ válida."""
        # IE do RJ válida (exemplo hipotético)
        assert ValidadorEmpresa._validar_ie_rj("12345678") is True
    
    def test_validar_inscricao_estadual(self):
        """Testa a validação de inscrição estadual por UF."""
        # Testa com UF válida
        assert ValidadorEmpresa.validar_inscricao_estadual("12345678", "RJ") is True
        
        # Testa com UF inválida (usa validação padrão)
        assert ValidadorEmpresa.validar_inscricao_estadual("12345", "XX") is True  # Aceita qualquer valor


class TestValidadorProcessoJudicial:
    """Testes para o validador de processos judiciais."""
    
    def test_validar_numero_processo_valido(self):
        """Testa a validação de número de processo válido."""
        # Formato CNJ: NNNNNNN-NN.NNNN.N.NN.NNNN
        assert ValidadorProcessoJudicial.validar_numero_processo("1234567-89.1234.5.67.8901") is True
    
    def test_validar_numero_processo_invalido(self):
        """Testa a validação de número de processo inválido."""
        assert ValidadorProcessoJudicial.validar_numero_processo("123.45.6789-0") is False  # Formato inválido
        assert ValidadorProcessoJudicial.validar_numero_processo("") is False  # Vazio
        assert ValidadorProcessoJudicial.validar_numero_processo("1234567-89.1234.5.67.8902") is False  # Dígitos verificadores inválidos


class TestValidadorNegocio:
    """Testes para o validador de negócio principal."""
    
    def test_validar_documento(self):
        """Testa a validação de documentos pelo tipo."""
        # CPF válido
        assert ValidadorNegocio.validar_documento(TipoDocumento.CPF, "529.982.247-25") is True
        
        # CNPJ válido
        assert ValidadorNegocio.validar_documento(TipoDocumento.CNPJ, "33.000.167/0001-01") is True
        
        # Outro tipo de documento (sempre retorna True se não estiver vazio)
        assert ValidadorNegocio.validar_documento(TipoDocumento.RG, "12.345.678-9") is True
        
        # Documento inválido para o tipo
        assert ValidadorNegocio.validar_documento(TipoDocumento.CPF, "33.000.167/0001-01") is False  # CNPJ como CPF
    
    def test_validar_modelo(self):
        """Testa a validação de modelos Pydantic."""
        # Cria um modelo de teste
        class TestModel(BaseModel):
            id: int
            name: str = Field(..., min_length=3)
            email: str = Field(..., regex=r'^[^@]+@[^@]+/.[^@]+$')
        
        # Modelo válido
        valid_model = TestModel(id=1, name="Test", email="test@example.com")
        
        # Testa com modelo válido
        try:
            ValidadorNegocio.validar_modelo(valid_model)
            assert True  # Não deve lançar exceção
        except Exception:
            assert False, "Não deveria lançar exceção para modelo válido"
        
        # Testa com modelo inválido
        invalid_model = TestModel(id=1, name="A", email="invalid-email")
        with pytest.raises(Exception):
            ValidadorNegocio.validar_modelo(invalid_model)

