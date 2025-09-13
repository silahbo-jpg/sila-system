"""
Pydantic models for Certidão de Nascimento (Birth Certificate) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class CertidaoNascimentoBase(BaseModel):
    """Base schema for Birth Certificate."""
    nome_crianca: str = Field(..., description="Nome completo da criança")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    hora_nascimento: str = Field(..., description="Hora de nascimento (HH:MM)")
    local_nascimento: str = Field(..., description="Local de nascimento")
    peso_nascimento: float = Field(..., description="Peso ao nascer (kg)")
    altura_nascimento: float = Field(..., description="Altura ao nascer (cm)")
    nome_pai: str = Field(..., description="Nome completo do pai")
    nome_mae: str = Field(..., description="Nome completo da mãe")
    estado_civil_pais: str = Field(..., description="Estado civil dos pais")
    residencia_pais: str = Field(..., description="Endereço de residência dos pais")
    distrito: str = Field(..., description="Distrito")
    posto_administrativo: str = Field(..., description="Posto Administrativo")
    localidade: str = Field(..., description="Localidade")
    bairro: str = Field(..., description="Bairro")
    telefone: str = Field(..., description="Número de telefone")
    email: str = Field(..., description="Endereço de email")
    documento_identificacao_pai: str = Field(..., description="Documento de identificação do pai")
    documento_identificacao_mae: str = Field(..., description="Documento de identificação da mãe")
    comprovativo_nascimento: str = Field(..., description="Comprovativo de nascimento")
    fotografia: str = Field(..., description="Fotografia")
    status: str = Field(default="pendente", description="Status do pedido")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

    @validator('data_nascimento', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                raise ValueError("Formato de data inválido. Use o formato YYYY-MM-DD")
        return value

class CertidaoNascimentoCreate(CertidaoNascimentoBase):
    """Schema for creating a new Birth Certificate request."""
    pass

class CertidaoNascimentoUpdate(BaseModel):
    """Schema for updating a Birth Certificate request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao_pai: Optional[str] = None
    documento_identificacao_mae: Optional[str] = None
    comprovativo_nascimento: Optional[str] = None
    fotografia: Optional[str] = None

class CertidaoNascimentoInDBBase(CertidaoNascimentoBase):
    """Base schema with common attributes for database operations."""
    id: int
    numero_registro: str
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class CertidaoNascimentoRead(CertidaoNascimentoInDBBase):
    """Schema for reading Birth Certificate data."""
    pass

class CertidaoNascimentoList(BaseResponse):
    """Schema for listing multiple Birth Certificate requests."""
    data: List[CertidaoNascimentoRead] = []
