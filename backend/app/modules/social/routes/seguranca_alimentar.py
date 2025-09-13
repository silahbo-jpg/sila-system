from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.seguranca_alimentar import SegurancaAlimentar
from app.modules.social.schemas.seguranca_alimentar import SegurancaAlimentarCreate, SegurancaAlimentarRead, SegurancaAlimentarUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/seguranca-alimentar", tags=["Segurança Alimentar"])

@router.post("/", response_model=SegurancaAlimentarRead)
def criar_seguranca_alimentar(
    data: SegurancaAlimentarCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Food Security / Criar novo Segurança Alimentar"""
    db_item = SegurancaAlimentar(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SegurancaAlimentarRead)
def obter_seguranca_alimentar(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Food Security by ID / Obter Segurança Alimentar por ID"""
    item = db.query(SegurancaAlimentar).filter(SegurancaAlimentar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Segurança Alimentar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SegurancaAlimentarRead])
def listar_seguranca_alimentar(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Food Security / Listar Segurança Alimentar"""
    return db.query(SegurancaAlimentar).filter(
        SegurancaAlimentar.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SegurancaAlimentarRead)
def atualizar_seguranca_alimentar(
    item_id: int, 
    data: SegurancaAlimentarUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Food Security / Atualizar Segurança Alimentar"""
    item = db.query(SegurancaAlimentar).filter(SegurancaAlimentar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Segurança Alimentar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
