from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.auxilio_social import AuxilioSocial
from app.modules.social.schemas.auxilio_social import AuxilioSocialCreate, AuxilioSocialRead, AuxilioSocialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/auxilio-social", tags=["Auxílio Social"])

@router.post("/", response_model=AuxilioSocialRead)
def criar_auxilio_social(
    data: AuxilioSocialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Social Assistance / Criar novo Auxílio Social"""
    db_item = AuxilioSocial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AuxilioSocialRead)
def obter_auxilio_social(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Social Assistance by ID / Obter Auxílio Social por ID"""
    item = db.query(AuxilioSocial).filter(AuxilioSocial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Auxílio Social não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AuxilioSocialRead])
def listar_auxilio_social(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Social Assistance / Listar Auxílio Social"""
    return db.query(AuxilioSocial).filter(
        AuxilioSocial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AuxilioSocialRead)
def atualizar_auxilio_social(
    item_id: int, 
    data: AuxilioSocialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Social Assistance / Atualizar Auxílio Social"""
    item = db.query(AuxilioSocial).filter(AuxilioSocial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Auxílio Social não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
