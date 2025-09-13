"""
Pydantic models for Visto de Permanência (Residence Permit) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class VistoPermanenciaBase(BaseModel):
    """Base schema for Residence Permit."""
    numero_bi: str = Field(..., description="Número do Bilhete de Identidade")
    nome_completo: str = Field(..., description="Nome completo do requerente")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    nacionalidade: str = Field(..., description="Nacionalidade")
    pais_origem: str = Field(..., description="País de origem")
    tipo_visto: str = Field(..., description="Tipo de visto solicitado")
    motivo: str = Field(..., description="Motivo do pedido de visto")
    data_entrada: date = Field(..., description="Data de entrada no país")
    documento_identificacao: str = Field(..., description="Número do documento de identificação")
    comprovativo_residencia: str = Field(..., description="Comprovativo de residência")
    fotografia: str = Field(..., description="Fotografia")
    status: str = Field(default="pendente", description="Status do pedido")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

    @validator('data_nascimento', 'data_entrada', pre=True)
    def parse_dates(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                raise ValueError("Formato de data inválido. Use o formato YYYY-MM-DD")
        return value

class VistoPermanenciaCreate(VistoPermanenciaBase):
    """Schema for creating a new Residence Permit request."""
    pass

class VistoPermanenciaUpdate(BaseModel):
    """Schema for updating a Residence Permit request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao: Optional[str] = None
    comprovativo_residencia: Optional[str] = None
    fotografia: Optional[str] = None

class VistoPermanenciaInDBBase(VistoPermanenciaBase):
    """Base schema with common attributes for database operations."""
    id: int
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class VistoPermanenciaRead(VistoPermanenciaInDBBase):
    """Schema for reading Residence Permit data."""
    pass

class VistoPermanenciaList(BaseResponse):
    """Schema for listing multiple Residence Permit requests."""
    data: List[VistoPermanenciaRead] = []
