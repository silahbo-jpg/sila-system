from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.plano_urbano import PlanoUrbano
from app.modules.urbanism.schemas.plano_urbano import PlanoUrbanoCreate, PlanoUrbanoRead, PlanoUrbanoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/plano-urbano", tags=["Plano Urbano Municipal"])

@router.post("/", response_model=PlanoUrbanoRead)
def criar_plano_urbano(
    data: PlanoUrbanoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Urban Plan / Criar novo Plano Urbano Municipal"""
    db_item = PlanoUrbano(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=PlanoUrbanoRead)
def obter_plano_urbano(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Urban Plan by ID / Obter Plano Urbano Municipal por ID"""
    item = db.query(PlanoUrbano).filter(PlanoUrbano.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Plano Urbano Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[PlanoUrbanoRead])
def listar_plano_urbano(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Urban Plan / Listar Plano Urbano Municipal"""
    return db.query(PlanoUrbano).filter(
        PlanoUrbano.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=PlanoUrbanoRead)
def atualizar_plano_urbano(
    item_id: int, 
    data: PlanoUrbanoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Urban Plan / Atualizar Plano Urbano Municipal"""
    item = db.query(PlanoUrbano).filter(PlanoUrbano.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Plano Urbano Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
