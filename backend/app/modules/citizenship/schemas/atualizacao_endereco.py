"""
Pydantic models for Atualização de Endereço (Address Update) operations.
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.schemas import BaseResponse

class AtualizacaoEnderecoBase(BaseModel):
    """Base schema for Address Update."""
    numero_bi: str = Field(..., description="Número do Bilhete de Identidade")
    nome_completo: str = Field(..., description="Nome completo do requerente")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    
    # Endereço antigo
    endereco_antigo: str = Field(..., description="Endereço antigo completo")
    distrito_antigo: str = Field(..., description="Distrito antigo")
    posto_administrativo_antigo: str = Field(..., description="Posto Administrativo antigo")
    localidade_antiga: str = Field(..., description="Localidade antiga")
    bairro_antigo: str = Field(..., description="Bairro antigo")
    
    # Novo endereço
    novo_endereco: str = Field(..., description="Novo endereço completo")
    novo_distrito: str = Field(..., description="Novo distrito")
    novo_posto_administrativo: str = Field(..., description="Novo Posto Administrativo")
    nova_localidade: str = Field(..., description="Nova localidade")
    novo_bairro: str = Field(..., description="Novo bairro")
    
    motivo_mudanca: str = Field(..., description="Motivo da mudança de endereço")
    data_mudanca: date = Field(..., description="Data da mudança (YYYY-MM-DD)")
    telefone: str = Field(..., description="Número de telefone")
    email: str = Field(..., description="Endereço de email")
    documento_identificacao: str = Field(..., description="Número do documento de identificação")
    comprovativo_residencia: str = Field(..., description="Comprovativo de residência")
    fotografia: str = Field(..., description="Fotografia")
    status: str = Field(default="pendente", description="Status do pedido")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

    @validator('data_nascimento', 'data_mudanca', pre=True)
    def parse_dates(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                raise ValueError("Formato de data inválido. Use o formato YYYY-MM-DD")
        return value

class AtualizacaoEnderecoCreate(AtualizacaoEnderecoBase):
    """Schema for creating a new Address Update request."""
    pass

class AtualizacaoEnderecoUpdate(BaseModel):
    """Schema for updating an Address Update request."""
    status: Optional[str] = None
    observacoes: Optional[str] = None
    documento_identificacao: Optional[str] = None
    comprovativo_residencia: Optional[str] = None
    fotografia: Optional[str] = None

class AtualizacaoEnderecoInDBBase(AtualizacaoEnderecoBase):
    """Base schema with common attributes for database operations."""
    id: int
    numero_processo: str
    municipe_id: int
    data_criacao: date
    data_atualizacao: date

    class Config:
        from_attributes = True

class AtualizacaoEnderecoRead(AtualizacaoEnderecoInDBBase):
    """Schema for reading Address Update data."""
    pass

class AtualizacaoEnderecoList(BaseResponse):
    """Schema for listing multiple Address Update requests."""
    data: List[AtualizacaoEnderecoRead] = []
