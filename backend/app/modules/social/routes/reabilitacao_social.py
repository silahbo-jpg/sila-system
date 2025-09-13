from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.reabilitacao_social import ReabilitacaoSocial
from app.modules.social.schemas.reabilitacao_social import ReabilitacaoSocialCreate, ReabilitacaoSocialRead, ReabilitacaoSocialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/reabilitacao-social", tags=["Reabilitação Social"])

@router.post("/", response_model=ReabilitacaoSocialRead)
def criar_reabilitacao_social(
    data: ReabilitacaoSocialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Social Rehabilitation / Criar novo Reabilitação Social"""
    db_item = ReabilitacaoSocial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ReabilitacaoSocialRead)
def obter_reabilitacao_social(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Social Rehabilitation by ID / Obter Reabilitação Social por ID"""
    item = db.query(ReabilitacaoSocial).filter(ReabilitacaoSocial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reabilitação Social não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ReabilitacaoSocialRead])
def listar_reabilitacao_social(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Social Rehabilitation / Listar Reabilitação Social"""
    return db.query(ReabilitacaoSocial).filter(
        ReabilitacaoSocial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ReabilitacaoSocialRead)
def atualizar_reabilitacao_social(
    item_id: int, 
    data: ReabilitacaoSocialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Social Rehabilitation / Atualizar Reabilitação Social"""
    item = db.query(ReabilitacaoSocial).filter(ReabilitacaoSocial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reabilitação Social não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
