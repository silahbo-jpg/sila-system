from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class AuditoriaLogCreate(BaseModel):
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None

class AuditoriaLogUpdate(BaseModel):
    nome: Optional[str] = None
    nome_en: Optional[str] = None
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: Optional[bool] = None
    status: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None

class AuditoriaLogRead(BaseModel):
    id: int
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    status: str
    dados_adicionais: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
