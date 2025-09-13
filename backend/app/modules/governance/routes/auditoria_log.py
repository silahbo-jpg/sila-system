from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.governance.models.auditoria_log import AuditoriaLog
from app.modules.governance.schemas.auditoria_log import AuditoriaLogCreate, AuditoriaLogRead, AuditoriaLogUpdate

router = APIRouter(prefix="/internal/auditoria-log", tags=["Auditoria de Log"])

@router.post("/", response_model=AuditoriaLogRead)
def criar_auditoria_log(data: AuditoriaLogCreate):
    """Create new Audit Logging / Criar novo Auditoria de Log"""
    db_item = AuditoriaLog(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AuditoriaLogRead)
def obter_auditoria_log(item_id: int):
    """Get Audit Logging by ID / Obter Auditoria de Log por ID"""
    item = db.query(AuditoriaLog).filter(AuditoriaLog.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Auditoria de Log não encontrado")
    return item

@router.get("/", response_model=List[AuditoriaLogRead])
def listar_auditoria_log(skip: int = 0, limit: int = 100):
    """List Audit Logging / Listar Auditoria de Log"""
    return db.query(AuditoriaLog).offset(skip).limit(limit).all()

@router.put("/id", response_model=AuditoriaLogRead)
def atualizar_auditoria_log(item_id: int, data: AuditoriaLogUpdate):
    """Update Audit Logging / Atualizar Auditoria de Log"""
    item = db.query(AuditoriaLog).filter(AuditoriaLog.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Auditoria de Log não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
