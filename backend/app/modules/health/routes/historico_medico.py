from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.historico_medico import HistoricoMedico
from app.modules.health.schemas.historico_medico import HistoricoMedicoCreate, HistoricoMedicoRead, HistoricoMedicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/historico-medico", tags=["Histórico Médico Digital"])

@router.post("/", response_model=HistoricoMedicoRead)
def criar_historico_medico(
    data: HistoricoMedicoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Digital Medical History / Criar novo Histórico Médico Digital"""
    db_item = HistoricoMedico(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=HistoricoMedicoRead)
def obter_historico_medico(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Digital Medical History by ID / Obter Histórico Médico Digital por ID"""
    item = db.query(HistoricoMedico).filter(HistoricoMedico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Histórico Médico Digital não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[HistoricoMedicoRead])
def listar_historico_medico(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Digital Medical History / Listar Histórico Médico Digital"""
    return db.query(HistoricoMedico).filter(
        HistoricoMedico.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=HistoricoMedicoRead)
def atualizar_historico_medico(
    item_id: int, 
    data: HistoricoMedicoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Digital Medical History / Atualizar Histórico Médico Digital"""
    item = db.query(HistoricoMedico).filter(HistoricoMedico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Histórico Médico Digital não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
