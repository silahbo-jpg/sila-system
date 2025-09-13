from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.micro_credito import MicroCredito
from app.modules.finance.schemas.micro_credito import MicroCreditoCreate, MicroCreditoRead, MicroCreditoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/micro-credito", tags=["Microcrédito Municipal"])

@router.post("/", response_model=MicroCreditoRead)
def criar_micro_credito(
    data: MicroCreditoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Microcredit / Criar novo Microcrédito Municipal"""
    db_item = MicroCredito(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MicroCreditoRead)
def obter_micro_credito(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Microcredit by ID / Obter Microcrédito Municipal por ID"""
    item = db.query(MicroCredito).filter(MicroCredito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Microcrédito Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[MicroCreditoRead])
def listar_micro_credito(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Microcredit / Listar Microcrédito Municipal"""
    return db.query(MicroCredito).filter(
        MicroCredito.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=MicroCreditoRead)
def atualizar_micro_credito(
    item_id: int, 
    data: MicroCreditoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Microcredit / Atualizar Microcrédito Municipal"""
    item = db.query(MicroCredito).filter(MicroCredito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Microcrédito Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
