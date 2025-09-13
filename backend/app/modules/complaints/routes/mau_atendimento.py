from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.mau_atendimento import MauAtendimento
from app.modules.complaints.schemas.mau_atendimento import MauAtendimentoCreate, MauAtendimentoRead, MauAtendimentoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/mau-atendimento", tags=["Mau Atendimento"])

@router.post("/", response_model=MauAtendimentoRead)
def criar_mau_atendimento(
    data: MauAtendimentoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Poor Service / Criar novo Mau Atendimento"""
    db_item = MauAtendimento(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MauAtendimentoRead)
def obter_mau_atendimento(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Poor Service by ID / Obter Mau Atendimento por ID"""
    item = db.query(MauAtendimento).filter(MauAtendimento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Mau Atendimento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[MauAtendimentoRead])
def listar_mau_atendimento(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Poor Service / Listar Mau Atendimento"""
    return db.query(MauAtendimento).filter(
        MauAtendimento.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=MauAtendimentoRead)
def atualizar_mau_atendimento(
    item_id: int, 
    data: MauAtendimentoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Poor Service / Atualizar Mau Atendimento"""
    item = db.query(MauAtendimento).filter(MauAtendimento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Mau Atendimento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
