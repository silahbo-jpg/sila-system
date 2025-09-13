from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.monitoramento_ambiental import MonitoramentoAmbiental
from app.modules.sanitation.schemas.monitoramento_ambiental import MonitoramentoAmbientalCreate, MonitoramentoAmbientalRead, MonitoramentoAmbientalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/monitoramento-ambiental", tags=["Monitoramento Ambiental"])

@router.post("/", response_model=MonitoramentoAmbientalRead)
def criar_monitoramento_ambiental(
    data: MonitoramentoAmbientalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Environmental Monitoring / Criar novo Monitoramento Ambiental"""
    db_item = MonitoramentoAmbiental(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MonitoramentoAmbientalRead)
def obter_monitoramento_ambiental(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Environmental Monitoring by ID / Obter Monitoramento Ambiental por ID"""
    item = db.query(MonitoramentoAmbiental).filter(MonitoramentoAmbiental.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Monitoramento Ambiental não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[MonitoramentoAmbientalRead])
def listar_monitoramento_ambiental(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Environmental Monitoring / Listar Monitoramento Ambiental"""
    return db.query(MonitoramentoAmbiental).filter(
        MonitoramentoAmbiental.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=MonitoramentoAmbientalRead)
def atualizar_monitoramento_ambiental(
    item_id: int, 
    data: MonitoramentoAmbientalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Environmental Monitoring / Atualizar Monitoramento Ambiental"""
    item = db.query(MonitoramentoAmbiental).filter(MonitoramentoAmbiental.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Monitoramento Ambiental não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
