"""
Pydantic models for Emissão de Bilhete de Identidade (ID Card Issuance) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class EmissaoBIBase(BaseModel):
    """Base schema for ID Card Issuance."""
    nome_completo: str = Field(..., description="Nome completo do requerente")
    nome_pai: str = Field(..., description="Nome do pai")
    nome_mae: str = Field(..., description="Nome da mãe")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    local_nascimento: str = Field(..., description="Local de nascimento")
    estado_civil: str = Field(..., description="Estado civil")
    genero: str = Field(..., description="Gênero")
    altura: str = Field(..., description="Altura em metros")
    residencia: str = Field(..., description="Endereço de residência")
    distrito: str = Field(..., description="Distrito")
    posto_administrativo: str = Field(..., description="Posto Administrativo")
    localidade: str = Field(..., description="Localidade")
    bairro: str = Field(..., description="Bairro")
    telefone: str = Field(..., description="Número de telefone")
    email: str = Field(..., description="Endereço de email")
    documento_identificacao: str = Field(..., description="Número do documento de identificação")
    comprovativo_residencia: str = Field(..., description="Comprovativo de residência")
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

class EmissaoBICreate(EmissaoBIBase):
    """Schema for creating a new ID Card Issuance request."""
    pass

class EmissaoBIUpdate(BaseModel):
    """Schema for updating an ID Card Issuance request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao: Optional[str] = None
    comprovativo_residencia: Optional[str] = None
    fotografia: Optional[str] = None

class EmissaoBIInDBBase(EmissaoBIBase):
    """Base schema with common attributes for database operations."""
    id: int
    numero_bi: str
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class EmissaoBIRead(EmissaoBIInDBBase):
    """Schema for reading ID Card Issuance data."""
    pass

class EmissaoBIList(BaseResponse):
    """Schema for listing multiple ID Card Issuance requests."""
    data: List[EmissaoBIRead] = []
