"""
Business logic for BI Update functionality.
This module contains the business rules and workflows specific to BI updates.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logging import get_structured_logger as get_logger
from app.modules.citizenship.models.atualizacao_b_i import AtualizacaoBI
from app.modules.citizenship.schemas.atualizacao_b_i import (
    AtualizacaoBICreate,
    AtualizacaoBIUpdate,
    DocumentType
)

logger = get_logger(__name__)

class BIStatus(str, Enum):
    DRAFT = "rascunho"
    PENDING = "pendente"
    UNDER_REVIEW = "em_analise"
    APPROVED = "aprovado"
    REJECTED = "rejeitado"
    PROCESSING = "em_processamento"
    COMPLETED = "concluido"
    CANCELLED = "cancelado"

class BIBusinessRules:
    """Business rules for BI update operations"""
    
    # Document type specific rules
    DOCUMENT_REQUIREMENTS = {
        DocumentType.BILHETE_IDENTIDADE: {
            "min_age": 16,
            "required_docs": ["foto_bi_atual", "comprovativo_morada"],
            "validity_years": 10,
        },
        DocumentType.CARTAO_CIDADAO: {
            "min_age": 0,  # No minimum age
            "required_docs": ["foto_bi_atual", "comprovativo_morada", "foto_rosto"],
            "validity_years": 5,
        },
        DocumentType.PASSAPORTE: {
            "min_age": 0,
            "required_docs": ["bi_valido", "comprovativo_morada", "foto_rosto"],
            "validity_years": 5,
        },
    }
    
    # Status transition rules
    ALLOWED_TRANSITIONS = {
        BIStatus.DRAFT: [BIStatus.PENDING, BIStatus.CANCELLED],
        BIStatus.PENDING: [BIStatus.UNDER_REVIEW, BIStatus.CANCELLED],
        BIStatus.UNDER_REVIEW: [BIStatus.APPROVED, BIStatus.REJECTED, BIStatus.PROCESSING],
        BIStatus.PROCESSING: [BIStatus.COMPLETED, BIStatus.REJECTED],
        BIStatus.APPROVED: [BIStatus.PROCESSING],
        # No transitions from these states
        BIStatus.REJECTED: [],
        BIStatus.COMPLETED: [],
        BIStatus.CANCELLED: [],
    }
    
    @classmethod
    def validate_document_requirements(
        cls, 
        document_type: DocumentType, 
        uploaded_docs: List[str], 
        birth_date: datetime
    ) -> Tuple[bool, List[str]]:
        """
        Validate if all required documents are provided for the given document type.
        Returns (is_valid, missing_docs)
        """
        requirements = cls.DOCUMENT_REQUIREMENTS.get(document_type, {})
        required_docs = set(requirements.get("required_docs", []))
        uploaded_docs = set(uploaded_docs or [])
        missing_docs = list(required_docs - uploaded_docs)
        
        # Check age requirements
        age = (datetime.now() - birth_date).days // 365
        if requirements.get("min_age", 0) > 0 and age < requirements["min_age"]:
            return False, [f"Minimum age requirement not met. Must be at least {requirements['min_age']} years old."]
        
        return len(missing_docs) == 0, missing_docs
    
    @classmethod
    def validate_status_transition(
        cls, 
        current_status: str, 
        new_status: str,
        user_role: str = "user"
    ) -> bool:
        """
        Validate if the status transition is allowed.
        
        Args:
            current_status: Current status of the request
            new_status: Desired new status
            user_role: Role of the user making the change
            
        Returns:
            bool: True if transition is valid, False otherwise
        """
        try:
            current = BIStatus(current_status.lower())
            new = BIStatus(new_status.lower())
        except ValueError:
            return False
            
        # Only admins can perform certain transitions
        if new in [BIStatus.APPROVED, BIStatus.REJECTED, BIStatus.PROCESSING] and user_role != "admin":
            return False
            
        return new in cls.ALLOWED_TRANSITIONS.get(current, [])
    
    @classmethod
    def calculate_expiry_date(cls, document_type: DocumentType) -> datetime:
        """Calculate the expiry date for a new document"""
        validity_years = cls.DOCUMENT_REQUIREMENTS.get(
            document_type, {}
        ).get("validity_years", 5)
        return datetime.now() + timedelta(days=validity_years * 365)
    
    @classmethod
    def get_next_available_number(
        cls, 
        db: Session, 
        document_type: DocumentType
    ) -> str:
        """Generate the next available document number"""
        # This is a simplified example - adjust based on your numbering scheme
        prefix = {
            DocumentType.BILHETE_IDENTIDADE: "BI",
            DocumentType.CARTAO_CIDADAO: "CC",
            DocumentType.PASSAPORTE: "PP"
        }.get(document_type, "DOC")
        
        # Get the highest existing number for this document type
        last_doc = db.query(AtualizacaoBI).filter(
            AtualizacaoBI.dados_adicionais["tipo_documento"].astext == document_type.value
        ).order_by(AtualizacaoBI.id.desc()).first()
        
        if last_doc and last_doc.dados_adicionais.get("numero_documento_gerado"):
            last_num = int(last_doc.dados_adicionais["numero_documento_gerado"][2:])
            next_num = last_num + 1
        else:
            next_num = 1
            
        return f"{prefix}{next_num:08d}"
        
    @classmethod
    def get_allowed_status_transitions(cls, current_status: str) -> List[str]:
        """
        Get a list of statuses that the current status can transition to.
        
        Args:
            current_status: The current status of the BI update request
            
        Returns:
            List of status strings that the current status can transition to
        """
        try:
            current = BIStatus(current_status.lower())
            return [status.value for status in cls.ALLOWED_TRANSITIONS.get(current, [])]
        except ValueError:
            return []
