"""
Pydantic models for Passport Issuance (Emissão de Passaporte) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class EmissaoPassaporteBase(BaseModel):
    """Base schema for Passport Issuance."""
    numero_bi: str = Field(..., description="Número do Bilhete de Identidade")
    nome_completo: str = Field(..., description="Nome completo do requerente")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    local_nascimento: str = Field(..., description="Local de nascimento")
    nome_pai: str = Field(..., description="Nome do pai")
    nome_mae: str = Field(..., description="Nome da mãe")
    estado_civil: str = Field(..., description="Estado civil")
    genero: str = Field(..., description="Gênero")
    altura: str = Field(..., description="Altura em metros")
    residencia: str = Field(..., description="Endereço de residência")
    telefone: str = Field(..., description="Número de telefone")
    email: str = Field(..., description="Endereço de email")
    motivo_viagem: str = Field(..., description="Motivo da viagem")
    pais_destino: str = Field(..., description="País de destino")
    data_prevista_viagem: date = Field(..., description="Data prevista para viagem")
    documento_identificacao: str = Field(..., description="Número do documento de identificação")
    comprovativo_residencia: str = Field(..., description="Comprovativo de residência")
    fotografia: str = Field(..., description="Fotografia")
    status: str = Field(default="pendente", description="Status do pedido")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

    @validator('data_nascimento', 'data_prevista_viagem', pre=True)
    def parse_dates(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                raise ValueError("Formato de data inválido. Use o formato YYYY-MM-DD")
        return value

class EmissaoPassaporteCreate(EmissaoPassaporteBase):
    """Schema for creating a new Passport Issuance request."""
    pass

class EmissaoPassaporteUpdate(BaseModel):
    """Schema for updating a Passport Issuance request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao: Optional[str] = None
    comprovativo_residencia: Optional[str] = None
    fotografia: Optional[str] = None

class EmissaoPassaporteInDBBase(EmissaoPassaporteBase):
    """Base schema with common attributes for database operations."""
    id: int
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class EmissaoPassaporteRead(EmissaoPassaporteInDBBase):
    """Schema for reading Passport Issuance data."""
    pass

class EmissaoPassaporteList(BaseResponse):
    """Schema for listing multiple Passport Issuance requests."""
    data: List[EmissaoPassaporteRead] = []
