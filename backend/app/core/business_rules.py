"""
Módulo centralizado de regras de negócio do sistema SILA.

Este módulo contém as regras de negócio que são compartilhadas entre diferentes
módulos da aplicação, garantindo consistência e evitando duplicação de código.
"""
from datetime import date, datetime, timedelta
from typing import Optional, Dict, Any, List, Type, TypeVar, Generic
from enum import Enum
import re

from pydantic import BaseModel, ValidationError, field_validator

from app.core.exceptions import BusinessRuleError, ValidationError as AppValidationError
from app.core.structured_logging import get_logger

# Tipo genérico para modelos Pydantic
T = TypeVar('T', bound=BaseModel)

class TipoDocumento(str, Enum):
    """Tipos de documentos aceitos no sistema."""
    CPF = "CPF"
    CNPJ = "CNPJ"
    RG = "RG"
    CNH = "CNH"
    TITULO_ELEITOR = "TITULO_ELEITOR"
    OUTRO = "OUTRO"

class ValidadorDocumentos:
    """Classe responsável por validar documentos oficiais."""
    
    # Cache LRU para armazenar CPFs já validados (max 1000 entradas)
    _cpf_cache = {}
    _cache_max_size = 1000
    _cache_hits = 0
    _cache_misses = 0
    _total_validations = 0
    _validation_errors = 0

    @classmethod
    def get_metrics(cls) -> dict:
        """Retorna métricas de desempenho da validação de CPF.
        
        Returns:
            dict: Dicionário com métricas de desempenho
        """
        cache_size = len(cls._cpf_cache)
        cache_hit_rate = (cls._cache_hits / cls._total_validations * 100) if cls._total_validations > 0 else 0
        
        return {
            'cache_size': cache_size,
            'cache_hits': cls._cache_hits,
            'cache_misses': cls._cache_misses,
            'cache_hit_rate': f"{cache_hit_rate:.2f}%",
            'total_validations': cls._total_validations,
            'validation_errors': cls._validation_errors,
            'error_rate': f"{(cls._validation_errors / cls._total_validations * 100) if cls._total_validations > 0 else 0:.2f}%"
        }

    @classmethod
    def _clear_cache(cls) -> None:
        """Limpa o cache de CPFs. Usado apenas para testes."""
        cls._cpf_cache.clear()
        cls._cache_hits = 0
        cls._cache_misses = 0
        cls._total_validations = 0
        cls._validation_errors = 0

    @classmethod
    def _add_to_cache(cls, cpf: str, is_valid: bool) -> None:
        """Adiciona um CPF ao cache, mantendo o tamanho máximo."""
        if len(cls._cpf_cache) >= cls._cache_max_size:
            # Remove o item mais antigo (FIFO)
            cls._cpf_cache.pop(next(iter(cls._cpf_cache)))
        cls._cpf_cache[cpf] = is_valid

    @classmethod
    def validar_cpf(cls, cpf: str) -> bool:
        """Valida um número de CPF com suporte a cache e métricas.
        
        Args:
            cpf: Número do CPF a ser validado (pode conter formatação)
            
        Returns:
            bool: True se o CPF for válido, False caso contrário
            
        Raises:
            ValueError: Se o CPF for nulo ou vazio
        """
        if not cpf:
            raise ValueError("CPF não pode ser vazio ou nulo")
            
        cls._total_validations += 1
        logger = get_logger(__name__)
        
        try:
            # Verifica se está no cache
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            
            if cpf_limpo in cls._cpf_cache:
                cls._cache_hits += 1
                logger.debug(f"CPF encontrado no cache: {cpf_limpo}")
                return cls._cpf_cache[cpf_limpo]
                
            cls._cache_misses += 1
            
            # Validação básica
            if len(cpf_limpo) != 11:
                logger.warning(f"CPF com tamanho inválido: {cpf_limpo}")
                cls._validation_errors += 1
                cls._add_to_cache(cpf_limpo, False)
                return False
                
            # Verifica se todos os dígitos são iguais
            if cpf_limpo == cpf_limpo[0] * 11:
                logger.warning(f"CPF com todos dígitos iguais: {cpf_limpo}")
                cls._validation_errors += 1
                cls._add_to_cache(cpf_limpo, False)
                return False
            
            # Cálculo do primeiro dígito verificador
            soma = 0
            for i in range(9):
                soma += int(cpf_limpo[i]) * (10 - i)
            
            resto = soma % 11
            digito1 = 0 if resto < 2 else 11 - resto
            
            # Cálculo do segundo dígito verificador
            soma = 0
            for i in range(10):
                multiplicador = 11 - i
                if i < 9:
                    soma += int(cpf_limpo[i]) * (multiplicador - 1)
                else:
                    soma += digito1 * 2
            
            resto = soma % 11
            digito2 = 0 if resto < 2 else 11 - resto
            
            # Verifica os dígitos verificadores
            if int(cpf_limpo[9]) == digito1 and int(cpf_limpo[10]) == digito2:
                logger.debug(f"CPF válido: {cpf_limpo}")
                cls._add_to_cache(cpf_limpo, True)
                return True
            else:
                logger.warning(f"CPF com dígitos verificadores inválidos: {cpf_limpo}")
                cls._validation_errors += 1
                cls._add_to_cache(cpf_limpo, False)
                return False
                
        except Exception as e:
            logger.error(f"Erro ao validar CPF {cpf}: {str(e)}", exc_info=True)
            cls._validation_errors += 1
            # Não adiciona ao cache em caso de erro inesperado
            return False
    
    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """Valida um número de CNPJ.
        
        Args:
            cnpj: Número do CNPJ a ser validado (apenas dígitos)
            
        Returns:
            bool: True se o CNPJ for válido, False caso contrário
        """
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
            
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
            
        # Cálculo do primeiro dígito verificador
        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(12):
            soma += int(cnpj[i]) * pesos[i]
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
            
        # Cálculo do segundo dígito verificador
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(13):
            soma += int(cnpj[i]) * pesos[i]
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
            
        # Verifica se os dígitos calculados conferem com os informados
        return int(cnpj[12]) == digito1 and int(cnpj[13]) == digito2


class ValidadorEndereco:
    """Classe responsável por validar endereços."""
    
    @staticmethod
    def validar_cep(cep: str) -> bool:
        """Valida um CEP brasileiro.
        
        Args:
            cep: CEP a ser validado (pode conter ou não formatação)
            
        Returns:
            bool: True se o CEP for válido, False caso contrário
        """
        # Remove caracteres não numéricos
        cep = re.sub(r'[^0-9]', '', cep)
        
        # Verifica se tem 8 dígitos
        if len(cep) != 8:
            return False
            
        # Verifica se todos os dígitos são iguais
        if cep == cep[0] * 8:
            return False
            
        return True


class ValidadorPessoa:
    """Classe responsável por validar dados de pessoas físicas."""
    
    @staticmethod
    def validar_data_nascimento(data: date) -> bool:
        """Valida uma data de nascimento.
        
        Args:
            data: Data de nascimento a ser validada
            
        Returns:
            bool: True se a data for válida, False caso contrário
        """
        hoje = date.today()
        idade = hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))
        
        # Verifica se a data não é no futuro
        if data > hoje:
            return False
            
        # Verifica se a idade está em um intervalo razoável (0 a 130 anos)
        return 0 <= idade <= 130
    
    @staticmethod
    def validar_nome(nome: str) -> bool:
        """Valida um nome de pessoa.
        
        Args:
            nome: Nome a ser validado
            
        Returns:
            bool: True se o nome for válido, False caso contrário
        """
        # Remove espaços extras e verifica se o nome tem pelo menos 3 caracteres
        nome = ' '.join(nome.strip().split())
        if len(nome) < 3:
            return False
            
        # Verifica se contém apenas letras, espaços e alguns caracteres especiais comuns em nomes
        if not re.match(r'^[\p{L}\s\'-]+$', nome, re.UNICODE):
            return False
            
        # Verifica se tem pelo menos um espaço (nome e sobrenome)
        if ' ' not in nome:
            return False
            
        return True


class ValidadorEmpresa:
    """Classe responsável por validar dados de empresas."""
    
    @staticmethod
    def validar_inscricao_estadual(ie: str, uf: str) -> bool:
        """Valida uma Inscrição Estadual de acordo com a UF.
        
        Args:
            ie: Número da Inscrição Estadual
            uf: Sigla da UF (ex: 'SP', 'RJ')
            
        Returns:
            bool: True se a IE for válida, False caso contrário
        """
        # Remove caracteres não numéricos e converte para maiúsculas
        ie = re.sub(r'[^0-9]', '', ie)
        uf = uf.upper()
        
        # Dicionário com os padrões de validação por UF
        # Cada entrada contém o tamanho esperado e a função de validação específica
        validadores = {
            'AC': (13, ValidadorEmpresa._validar_ie_ac),
            'AL': (9, ValidadorEmpresa._validar_ie_al),
            # Adicione os outros estados conforme necessário
            'SP': (12, ValidadorEmpresa._validar_ie_sp),
            'RJ': (8, ValidadorEmpresa._validar_ie_rj),
            # Padrão genérico para estados não implementados
            'DEFAULT': (lambda x: 5 <= len(x) <= 14, lambda x: True)
        }
        
        # Obtém o validador para a UF ou o padrão
        tamanho_esperado, validador = validadores.get(uf, validadores['DEFAULT'])
        
        # Verifica o tamanho
        if callable(tamanho_esperado):
            if not tamanho_esperado(ie):
                return False
        elif len(ie) != tamanho_esperado:
            return False
            
        # Aplica a validação específica
        return validador(ie)
    
    @staticmethod
    def _validar_ie_sp(ie: str) -> bool:
        """Valida Inscrição Estadual de São Paulo."""
        # Remove caracteres não numéricos
        ie = re.sub(r'[^0-9]', '', ie)
        
        # Verifica o tamanho
        if len(ie) != 12:
            return False
            
        # Cálculo do primeiro dígito verificador
        pesos = [1, 3, 4, 5, 6, 7, 8, 10]
        soma = 0
        for i in range(8):
            soma += int(ie[i]) * pesos[i]
        resto = soma % 11
        digito1 = 0 if resto == 10 else resto
        
        # Cálculo do segundo dígito verificador
        pesos = [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(11):
            soma += int(ie[i]) * pesos[i]
        resto = soma % 11
        digito2 = 0 if resto == 10 else resto
        
        return int(ie[8]) == digito1 and int(ie[11]) == digito2
    
    @staticmethod
    def _validar_ie_rj(ie: str) -> bool:
        """Valida Inscrição Estadual do Rio de Janeiro."""
        # Remove caracteres não numéricos
        ie = re.sub(r'[^0-9]', '', ie)
        
        # Verifica o tamanho
        if len(ie) != 8:
            return False
            
        # Cálculo do dígito verificador
        pesos = [2, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(7):
            soma += int(ie[i]) * pesos[i]
        resto = soma % 11
        digito = 0 if resto <= 1 else 11 - resto
        
        return int(ie[7]) == digito
    
    # Implementações simplificadas para outros estados
    @staticmethod
    def _validar_ie_ac(ie: str) -> bool:
        """Valida Inscrição Estadual do Acre."""
        return len(ie) == 13 and ie.startswith('01')
    
    @staticmethod
    def _validar_ie_al(ie: str) -> bool:
        """Valida Inscrição Estadual de Alagoas."""
        return len(ie) == 9 and ie.startswith('24')


class ValidadorProcessoJudicial:
    """Classe responsável por validar números de processo judicial."""
    
    @staticmethod
    def validar_numero_processo(numero: str) -> bool:
        """Valida um número de processo judicial no padrão CNJ.
        
        Args:
            numero: Número do processo no formato NNNNNNN-NN.NNNN.N.NN.NNNN
            
        Returns:
            bool: True se o número for válido, False caso contrário
        """
        # Verifica o formato básico com regex
        padrao = r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$'
        if not re.match(padrao, numero):
            return False
            
        # Remove caracteres não numéricos para cálculo dos verificadores
        digitos = re.sub(r'[^0-9]', '', numero)
        
        # Obtém os dígitos verificadores (8º e 9º dígitos)
        dv1 = int(digitos[7])
        dv2 = int(digitos[8])
        
        # Cálculo do primeiro dígito verificador
        soma = 0
        for i in range(7):
            soma += int(digitos[i]) * (8 - i)
        resto = soma % 11
        dv1_calculado = 0 if resto == 0 or resto == 1 else 11 - resto
        
        # Cálculo do segundo dígito verificador
        soma = 0
        for i in range(8):
            soma += int(digitos[i]) * (9 - i)
        soma += dv1_calculado * 2
        resto = soma % 11
        dv2_calculado = 0 if resto == 0 or resto == 1 else 11 - resto
        
        return dv1 == dv1_calculado and dv2 == dv2_calculado


class ValidadorNegocio:
    """Classe principal para validações de negócio.
    
    Esta classe fornece uma interface unificada para todas as validações de negócio
    do sistema, delegando para as classes especializadas conforme necessário.
    """
    
    # Instâncias dos validadores
    documento = ValidadorDocumentos()
    endereco = ValidadorEndereco()
    pessoa = ValidadorPessoa()
    empresa = ValidadorEmpresa()
    processo = ValidadorProcessoJudicial()
    
    @classmethod
    def validar_documento(cls, tipo: TipoDocumento, numero: str) -> bool:
        """Valida um documento com base no seu tipo.
        
        Args:
            tipo: Tipo do documento (CPF, CNPJ, etc.)
            numero: Número do documento a ser validado
            
        Returns:
            bool: True se o documento for válido, False caso contrário
        """
        if not numero:
            return False
            
        if tipo == TipoDocumento.CPF:
            return cls.documento.validar_cpf(numero)
        elif tipo == TipoDocumento.CNPJ:
            return cls.documento.validar_cnpj(numero)
        # Adicione outros tipos de documento conforme necessário
        
        # Para outros tipos de documento, apenas verifica se não está vazio
        return bool(numero.strip())
    
    @classmethod
    def validar_modelo(cls, modelo: T) -> None:
        """Valida um modelo Pydantic de acordo com as regras de negócio.
        
        Esta é uma extensão das validações do Pydantic para incluir regras
        de negócio mais complexas que não podem ser expressas apenas com
        os validadores padrão do Pydantic.
        
        Args:
            modelo: Instância do modelo Pydantic a ser validada
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
            ValidationError: Se houver erros de validação
        """
        # Primeiro valida o modelo com o Pydantic
        try:
            modelo.model_validate(modelo.model_dump())
        except ValidationError as e:
            raise AppValidationError("Erro de validação do modelo", errors=e.errors())
        
        # Aqui você pode adicionar validações de negócio específicas
        # baseadas no tipo do modelo
        model_name = modelo.__class__.__name__
        
        if model_name == "JudicialCertificateCreate":
            # Exemplo de validação específica para certificados judiciais
            if not cls.documento.validar_cpf(str(modelo.citizen_id)):
                raise BusinessRuleError("ID do cidadão inválido")
        
        # Adicione outras validações específicas por modelo aqui

