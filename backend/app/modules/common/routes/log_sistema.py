from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.common.models.log_sistema import LogSistema
from app.modules.common.schemas.log_sistema import LogSistemaCreate, LogSistemaRead, LogSistemaUpdate

router = APIRouter(prefix="/internal/log-sistema", tags=["Log do Sistema"])

@router.post("/", response_model=LogSistemaRead)
def criar_log_sistema(data: LogSistemaCreate):
    """Create new System Logging / Criar novo Log do Sistema"""
    db_item = LogSistema(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LogSistemaRead)
def obter_log_sistema(item_id: int):
    """Get System Logging by ID / Obter Log do Sistema por ID"""
    item = db.query(LogSistema).filter(LogSistema.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Log do Sistema não encontrado")
    return item

@router.get("/", response_model=List[LogSistemaRead])
def listar_log_sistema(skip: int = 0, limit: int = 100):
    """List System Logging / Listar Log do Sistema"""
    return db.query(LogSistema).offset(skip).limit(limit).all()

@router.put("/id", response_model=LogSistemaRead)
def atualizar_log_sistema(item_id: int, data: LogSistemaUpdate):
    """Update System Logging / Atualizar Log do Sistema"""
    item = db.query(LogSistema).filter(LogSistema.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Log do Sistema não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
