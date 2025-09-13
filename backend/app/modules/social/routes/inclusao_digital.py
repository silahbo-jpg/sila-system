from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.inclusao_digital import InclusaoDigital
from app.modules.social.schemas.inclusao_digital import InclusaoDigitalCreate, InclusaoDigitalRead, InclusaoDigitalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/inclusao-digital", tags=["Inclusão Digital"])

@router.post("/", response_model=InclusaoDigitalRead)
def criar_inclusao_digital(
    data: InclusaoDigitalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Digital Inclusion / Criar novo Inclusão Digital"""
    db_item = InclusaoDigital(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=InclusaoDigitalRead)
def obter_inclusao_digital(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Digital Inclusion by ID / Obter Inclusão Digital por ID"""
    item = db.query(InclusaoDigital).filter(InclusaoDigital.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inclusão Digital não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[InclusaoDigitalRead])
def listar_inclusao_digital(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Digital Inclusion / Listar Inclusão Digital"""
    return db.query(InclusaoDigital).filter(
        InclusaoDigital.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=InclusaoDigitalRead)
def atualizar_inclusao_digital(
    item_id: int, 
    data: InclusaoDigitalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Digital Inclusion / Atualizar Inclusão Digital"""
    item = db.query(InclusaoDigital).filter(InclusaoDigital.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inclusão Digital não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
