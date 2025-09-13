from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.documents.models.assinatura_digital import AssinaturaDigital
from app.modules.documents.schemas.assinatura_digital import AssinaturaDigitalCreate, AssinaturaDigitalRead, AssinaturaDigitalUpdate

router = APIRouter(prefix="/internal/assinatura-digital", tags=["Assinatura Digital"])

@router.post("/", response_model=AssinaturaDigitalRead)
def criar_assinatura_digital(data: AssinaturaDigitalCreate):
    """Create new Digital Signature / Criar novo Assinatura Digital"""
    db_item = AssinaturaDigital(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AssinaturaDigitalRead)
def obter_assinatura_digital(item_id: int):
    """Get Digital Signature by ID / Obter Assinatura Digital por ID"""
    item = db.query(AssinaturaDigital).filter(AssinaturaDigital.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assinatura Digital não encontrado")
    return item

@router.get("/", response_model=List[AssinaturaDigitalRead])
def listar_assinatura_digital(skip: int = 0, limit: int = 100):
    """List Digital Signature / Listar Assinatura Digital"""
    return db.query(AssinaturaDigital).offset(skip).limit(limit).all()

@router.put("/id", response_model=AssinaturaDigitalRead)
def atualizar_assinatura_digital(item_id: int, data: AssinaturaDigitalUpdate):
    """Update Digital Signature / Atualizar Assinatura Digital"""
    item = db.query(AssinaturaDigital).filter(AssinaturaDigital.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assinatura Digital não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
