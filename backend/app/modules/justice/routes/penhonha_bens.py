from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.penhonha_bens import PenhonhaBens
from app.modules.justice.schemas.penhonha_bens import PenhonhaBensCreate, PenhonhaBensRead, PenhonhaBensUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/penhonha-bens", tags=["Penhora de Bens"])

@router.post("/", response_model=PenhonhaBensRead)
def criar_penhonha_bens(
    data: PenhonhaBensCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Asset Seizure / Criar novo Penhora de Bens"""
    db_item = PenhonhaBens(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=PenhonhaBensRead)
def obter_penhonha_bens(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Asset Seizure by ID / Obter Penhora de Bens por ID"""
    item = db.query(PenhonhaBens).filter(PenhonhaBens.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Penhora de Bens não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[PenhonhaBensRead])
def listar_penhonha_bens(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Asset Seizure / Listar Penhora de Bens"""
    return db.query(PenhonhaBens).filter(
        PenhonhaBens.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=PenhonhaBensRead)
def atualizar_penhonha_bens(
    item_id: int, 
    data: PenhonhaBensUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Asset Seizure / Atualizar Penhora de Bens"""
    item = db.query(PenhonhaBens).filter(PenhonhaBens.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Penhora de Bens não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
