"""CRUD operations for the justice module."""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import models
from . import schemas

def create_certificate(db: Session, certificate: schemas.JudicialCertificateCreate) -> models.JudicialCertificate:
    """Create a new judicial certificate."""
    db_certificate = models.JudicialCertificate(
        citizen_id=certificate.citizen_id,
        type=certificate.type,
        status=certificate.status,
        notes=certificate.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def get_certificate(db: Session, certificate_id: int) -> Optional[models.JudicialCertificate]:
    """Get a judicial certificate by ID."""
    return db.query(models.JudicialCertificate).filter(
        models.JudicialCertificate.id == certificate_id
    ).first()

def get_certificates(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    citizen_id: Optional[int] = None,
    status: Optional[schemas.CertificateStatus] = None
) -> List[models.JudicialCertificate]:
    """Get a list of judicial certificates with optional filtering."""
    query = db.query(models.JudicialCertificate)
    
    if citizen_id is not None:
        query = query.filter(models.JudicialCertificate.citizen_id == citizen_id)
    if status is not None:
        query = query.filter(models.JudicialCertificate.status == status)
        
    return query.offset(skip).limit(limit).all()

def update_certificate(
    db: Session, 
    db_certificate: models.JudicialCertificate,
    certificate_update: schemas.JudicialCertificateUpdate
) -> models.JudicialCertificate:
    """Update a judicial certificate."""
    update_data = certificate_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_certificate, field, value)
    
    db_certificate.updated_at = datetime.utcnow()
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def delete_certificate(db: Session, certificate_id: int) -> bool:
    """Delete a judicial certificate."""
    db_certificate = get_certificate(db, certificate_id)
    if db_certificate is None:
        return False
    
    db.delete(db_certificate)
    db.commit()
    return True
