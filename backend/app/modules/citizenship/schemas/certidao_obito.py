"""
Pydantic models for Certidão de Óbito (Death Certificate) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class CertidaoObitoBase(BaseModel):
    """Base schema for Death Certificate."""
    nome_falecido: str = Field(..., description="Nome completo do falecido")
    nome_pai: str = Field(..., description="Nome do pai")
    nome_mae: str = Field(..., description="Nome da mãe")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    data_obito: date = Field(..., description="Data do óbito (YYYY-MM-DD)")
    local_obito: str = Field(..., description="Local do óbito")
    causa_morte: str = Field(..., description="Causa da morte")
    estado_civil: str = Field(..., description="Estado civil")
    genero: str = Field(..., description="Gênero")
    naturalidade: str = Field(..., description="Naturalidade")
    residencia: str = Field(..., description="Último endereço de residência")
    distrito: str = Field(..., description="Distrito")
    posto_administrativo: str = Field(..., description="Posto Administrativo")
    localidade: str = Field(..., description="Localidade")
    bairro: str = Field(..., description="Bairro")
    nome_requerente: str = Field(..., description="Nome do requerente")
    parentesco: str = Field(..., description="Parentesco com o falecido")
    telefone: str = Field(..., description="Número de telefone")
    email: str = Field(..., description="Endereço de email")
    documento_identificacao: str = Field(..., description="Número do documento de identificação")
    comprovativo_obito: str = Field(..., description="Comprovativo de óbito")
    fotografia: str = Field(..., description="Fotografia")
    status: str = Field(default="pendente", description="Status do pedido")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

    @validator('data_nascimento', 'data_obito', pre=True)
    def parse_dates(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                raise ValueError("Formato de data inválido. Use o formato YYYY-MM-DD")
        return value

class CertidaoObitoCreate(CertidaoObitoBase):
    """Schema for creating a new Death Certificate request."""
    pass

class CertidaoObitoUpdate(BaseModel):
    """Schema for updating a Death Certificate request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao: Optional[str] = None
    comprovativo_obito: Optional[str] = None
    fotografia: Optional[str] = None

class CertidaoObitoInDBBase(CertidaoObitoBase):
    """Base schema with common attributes for database operations."""
    id: int
    numero_registro: str
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class CertidaoObitoRead(CertidaoObitoInDBBase):
    """Schema for reading Death Certificate data."""
    pass

class CertidaoObitoList(BaseResponse):
    """Schema for listing multiple Death Certificate requests."""
    data: List[CertidaoObitoRead] = []
