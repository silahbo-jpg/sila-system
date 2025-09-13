from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.consulta_telematica import ConsultaTelematica
from app.modules.health.schemas.consulta_telematica import ConsultaTelematicaCreate, ConsultaTelematicaRead, ConsultaTelematicaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/consulta-telematica", tags=["Teleconsulta Médica"])

@router.post("/", response_model=ConsultaTelematicaRead)
def criar_consulta_telematica(
    data: ConsultaTelematicaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Telemedicine Consultation / Criar novo Teleconsulta Médica"""
    db_item = ConsultaTelematica(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ConsultaTelematicaRead)
def obter_consulta_telematica(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Telemedicine Consultation by ID / Obter Teleconsulta Médica por ID"""
    item = db.query(ConsultaTelematica).filter(ConsultaTelematica.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Teleconsulta Médica não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ConsultaTelematicaRead])
def listar_consulta_telematica(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Telemedicine Consultation / Listar Teleconsulta Médica"""
    return db.query(ConsultaTelematica).filter(
        ConsultaTelematica.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ConsultaTelematicaRead)
def atualizar_consulta_telematica(
    item_id: int, 
    data: ConsultaTelematicaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Telemedicine Consultation / Atualizar Teleconsulta Médica"""
    item = db.query(ConsultaTelematica).filter(ConsultaTelematica.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Teleconsulta Médica não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
