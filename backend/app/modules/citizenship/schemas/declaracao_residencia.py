"""
Pydantic models for Declaração de Residência (Residence Certificate) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class DeclaracaoResidenciaBase(BaseModel):
    """Base schema for Residence Certificate."""
    numero_bi: str = Field(..., description="Número do Bilhete de Identidade")
    nome_completo: str = Field(..., description="Nome completo do requerente")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    nome_pai: str = Field(..., description="Nome do pai")
    nome_mae: str = Field(..., description="Nome da mãe")
    estado_civil: str = Field(..., description="Estado civil")
    genero: str = Field(..., description="Gênero")
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

class DeclaracaoResidenciaCreate(DeclaracaoResidenciaBase):
    """Schema for creating a new Residence Certificate request."""
    pass

class DeclaracaoResidenciaUpdate(BaseModel):
    """Schema for updating a Residence Certificate request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao: Optional[str] = None
    comprovativo_residencia: Optional[str] = None
    fotografia: Optional[str] = None

class DeclaracaoResidenciaInDBBase(DeclaracaoResidenciaBase):
    """Base schema with common attributes for database operations."""
    id: int
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class DeclaracaoResidenciaRead(DeclaracaoResidenciaInDBBase):
    """Schema for reading Residence Certificate data."""
    pass

class DeclaracaoResidenciaList(BaseResponse):
    """Schema for listing multiple Residence Certificate requests."""
    data: List[DeclaracaoResidenciaRead] = []
