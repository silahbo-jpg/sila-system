"""Pydantic schemas for the justice module."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class CertificateType(str, Enum):
    ANTECEDENTES = "Antecedentes"
    PROTESTOS = "Protestos"
    CRIMINAL = "Registo Criminal"
    PENHORA = "Certidão de Penhora"

class CertificateStatus(str, Enum):
    PENDING = "Pending"
    ISSUED = "Issued"
    REJECTED = "Rejected"
    EXPIRED = "Expired"

class JudicialCertificateBase(BaseModel):
    """Base schema for judicial certificates."""
    citizen_id: int = Field(..., description="ID do cidadão")
    type: CertificateType = Field(..., description="Tipo de certidão")
    status: CertificateStatus = Field(default=CertificateStatus.PENDING, description="Status da certidão")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class JudicialCertificateCreate(JudicialCertificateBase):
    """Schema for creating a new judicial certificate."""
    pass

class JudicialCertificateUpdate(BaseModel):
    """Schema for updating an existing judicial certificate."""
    status: Optional[CertificateStatus] = None
    notes: Optional[str] = None

class JudicialCertificateInDBBase(JudicialCertificateBase):
    """Base schema for judicial certificate in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JudicialCertificate(JudicialCertificateInDBBase):
    """Schema for returning a judicial certificate."""
    pass

class JudicialCertificateInDB(JudicialCertificateInDBBase):
    """Schema for judicial certificate stored in database."""
    pass
