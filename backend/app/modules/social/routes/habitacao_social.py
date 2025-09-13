from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.habitacao_social import HabitacaoSocial
from app.modules.social.schemas.habitacao_social import HabitacaoSocialCreate, HabitacaoSocialRead, HabitacaoSocialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/habitacao-social", tags=["Habitação Social"])

@router.post("/", response_model=HabitacaoSocialRead)
def criar_habitacao_social(
    data: HabitacaoSocialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Social Housing / Criar novo Habitação Social"""
    db_item = HabitacaoSocial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=HabitacaoSocialRead)
def obter_habitacao_social(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Social Housing by ID / Obter Habitação Social por ID"""
    item = db.query(HabitacaoSocial).filter(HabitacaoSocial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Habitação Social não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[HabitacaoSocialRead])
def listar_habitacao_social(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Social Housing / Listar Habitação Social"""
    return db.query(HabitacaoSocial).filter(
        HabitacaoSocial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=HabitacaoSocialRead)
def atualizar_habitacao_social(
    item_id: int, 
    data: HabitacaoSocialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Social Housing / Atualizar Habitação Social"""
    item = db.query(HabitacaoSocial).filter(HabitacaoSocial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Habitação Social não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
