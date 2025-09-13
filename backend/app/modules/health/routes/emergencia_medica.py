from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.emergencia_medica import EmergenciaMedica
from app.modules.health.schemas.emergencia_medica import EmergenciaMedicaCreate, EmergenciaMedicaRead, EmergenciaMedicaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/emergencia-medica", tags=["Serviço de Emergência Médica"])

@router.post("/", response_model=EmergenciaMedicaRead)
def criar_emergencia_medica(
    data: EmergenciaMedicaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Medical Emergency Service / Criar novo Serviço de Emergência Médica"""
    db_item = EmergenciaMedica(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EmergenciaMedicaRead)
def obter_emergencia_medica(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Medical Emergency Service by ID / Obter Serviço de Emergência Médica por ID"""
    item = db.query(EmergenciaMedica).filter(EmergenciaMedica.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Serviço de Emergência Médica não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EmergenciaMedicaRead])
def listar_emergencia_medica(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Medical Emergency Service / Listar Serviço de Emergência Médica"""
    return db.query(EmergenciaMedica).filter(
        EmergenciaMedica.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EmergenciaMedicaRead)
def atualizar_emergencia_medica(
    item_id: int, 
    data: EmergenciaMedicaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Medical Emergency Service / Atualizar Serviço de Emergência Médica"""
    item = db.query(EmergenciaMedica).filter(EmergenciaMedica.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Serviço de Emergência Médica não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
