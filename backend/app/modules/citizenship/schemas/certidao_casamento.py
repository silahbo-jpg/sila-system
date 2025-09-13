"""
Pydantic models for Certidão de Casamento (Marriage Certificate) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class CertidaoCasamentoBase(BaseModel):
    """Base schema for Marriage Certificate."""
    # Dados do primeiro cônjuge
    nome_conjuge1: str = Field(..., description="Nome completo do primeiro cônjuge")
    data_nascimento_conjuge1: date = Field(..., description="Data de nascimento do primeiro cônjuge (YYYY-MM-DD)")
    nacionalidade_conjuge1: str = Field(..., description="Nacionalidade do primeiro cônjuge")
    profissao_conjuge1: str = Field(..., description="Profissão do primeiro cônjuge")
    residencia_conjuge1: str = Field(..., description="Endereço do primeiro cônjuge")
    estado_civil_anterior_conjuge1: str = Field(..., description="Estado civil anterior do primeiro cônjuge")
    documento_identificacao_conjuge1: str = Field(..., description="Documento de identificação do primeiro cônjuge")

    # Dados do segundo cônjuge
    nome_conjuge2: str = Field(..., description="Nome completo do segundo cônjuge")
    data_nascimento_conjuge2: date = Field(..., description="Data de nascimento do segundo cônjuge (YYYY-MM-DD)")
    nacionalidade_conjuge2: str = Field(..., description="Nacionalidade do segundo cônjuge")
    profissao_conjuge2: str = Field(..., description="Profissão do segundo cônjuge")
    residencia_conjuge2: str = Field(..., description="Endereço do segundo cônjuge")
    estado_civil_anterior_conjuge2: str = Field(..., description="Estado civil anterior do segundo cônjuge")
    documento_identificacao_conjuge2: str = Field(..., description="Documento de identificação do segundo cônjuge")

    # Dados do casamento
    data_casamento: date = Field(..., description="Data do casamento (YYYY-MM-DD)")
    local_casamento: str = Field(..., description="Local do casamento")
    regime_bens: str = Field(..., description="Regime de bens do casamento")
    distrito: str = Field(..., description="Distrito")
    posto_administrativo: str = Field(..., description="Posto Administrativo")
    localidade: str = Field(..., description="Localidade")
    bairro: str = Field(..., description="Bairro")
    telefone: str = Field(..., description="Número de telefone")
    email: str = Field(..., description="Endereço de email")
    comprovativo_casamento: str = Field(..., description="Comprovativo de casamento")
    fotografia_conjuge1: str = Field(..., description="Fotografia do primeiro cônjuge")
    fotografia_conjuge2: str = Field(..., description="Fotografia do segundo cônjuge")
    status: str = Field(default="pendente", description="Status do pedido")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

    @validator('data_nascimento_conjuge1', 'data_nascimento_conjuge2', 'data_casamento', pre=True)
    def parse_dates(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                raise ValueError("Formato de data inválido. Use o formato YYYY-MM-DD")
        return value

class CertidaoCasamentoCreate(CertidaoCasamentoBase):
    """Schema for creating a new Marriage Certificate request."""
    pass

class CertidaoCasamentoUpdate(BaseModel):
    """Schema for updating a Marriage Certificate request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao_conjuge1: Optional[str] = None
    documento_identificacao_conjuge2: Optional[str] = None
    comprovativo_casamento: Optional[str] = None
    fotografia_conjuge1: Optional[str] = None
    fotografia_conjuge2: Optional[str] = None

class CertidaoCasamentoInDBBase(CertidaoCasamentoBase):
    """Base schema with common attributes for database operations."""
    id: int
    numero_registro: str
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class CertidaoCasamentoRead(CertidaoCasamentoInDBBase):
    """Schema for reading Marriage Certificate data."""
    pass

class CertidaoCasamentoList(BaseResponse):
    """Schema for listing multiple Marriage Certificate requests."""
    data: List[CertidaoCasamentoRead] = []
