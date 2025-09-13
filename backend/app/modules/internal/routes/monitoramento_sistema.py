from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.internal.models.monitoramento_sistema import MonitoramentoSistema
from app.modules.internal.schemas.monitoramento_sistema import MonitoramentoSistemaCreate, MonitoramentoSistemaRead, MonitoramentoSistemaUpdate

router = APIRouter(prefix="/internal/monitoramento-sistema", tags=["Monitoramento do Sistema"])

@router.post("/", response_model=MonitoramentoSistemaRead)
def criar_monitoramento_sistema(data: MonitoramentoSistemaCreate):
    """Create new System Monitoring / Criar novo Monitoramento do Sistema"""
    db_item = MonitoramentoSistema(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MonitoramentoSistemaRead)
def obter_monitoramento_sistema(item_id: int):
    """Get System Monitoring by ID / Obter Monitoramento do Sistema por ID"""
    item = db.query(MonitoramentoSistema).filter(MonitoramentoSistema.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Monitoramento do Sistema não encontrado")
    return item

@router.get("/", response_model=List[MonitoramentoSistemaRead])
def listar_monitoramento_sistema(skip: int = 0, limit: int = 100):
    """List System Monitoring / Listar Monitoramento do Sistema"""
    return db.query(MonitoramentoSistema).offset(skip).limit(limit).all()

@router.put("/id", response_model=MonitoramentoSistemaRead)
def atualizar_monitoramento_sistema(item_id: int, data: MonitoramentoSistemaUpdate):
    """Update System Monitoring / Atualizar Monitoramento do Sistema"""
    item = db.query(MonitoramentoSistema).filter(MonitoramentoSistema.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Monitoramento do Sistema não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
