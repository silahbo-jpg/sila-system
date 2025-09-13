from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.parcelamento_debito import ParcelamentoDebito
from app.modules.finance.schemas.parcelamento_debito import ParcelamentoDebitoCreate, ParcelamentoDebitoRead, ParcelamentoDebitoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/parcelamento-debito", tags=["Parcelamento de Débitos"])

@router.post("/", response_model=ParcelamentoDebitoRead)
def criar_parcelamento_debito(
    data: ParcelamentoDebitoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Debt Installment / Criar novo Parcelamento de Débitos"""
    db_item = ParcelamentoDebito(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ParcelamentoDebitoRead)
def obter_parcelamento_debito(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Debt Installment by ID / Obter Parcelamento de Débitos por ID"""
    item = db.query(ParcelamentoDebito).filter(ParcelamentoDebito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Parcelamento de Débitos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ParcelamentoDebitoRead])
def listar_parcelamento_debito(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Debt Installment / Listar Parcelamento de Débitos"""
    return db.query(ParcelamentoDebito).filter(
        ParcelamentoDebito.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ParcelamentoDebitoRead)
def atualizar_parcelamento_debito(
    item_id: int, 
    data: ParcelamentoDebitoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Debt Installment / Atualizar Parcelamento de Débitos"""
    item = db.query(ParcelamentoDebito).filter(ParcelamentoDebito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Parcelamento de Débitos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
