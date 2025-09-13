from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.irregularidade_fiscal import IrregularidadeFiscal
from app.modules.complaints.schemas.irregularidade_fiscal import IrregularidadeFiscalCreate, IrregularidadeFiscalRead, IrregularidadeFiscalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/irregularidade-fiscal", tags=["Irregularidade Fiscal"])

@router.post("/", response_model=IrregularidadeFiscalRead)
def criar_irregularidade_fiscal(
    data: IrregularidadeFiscalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Tax Irregularity / Criar novo Irregularidade Fiscal"""
    db_item = IrregularidadeFiscal(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=IrregularidadeFiscalRead)
def obter_irregularidade_fiscal(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Tax Irregularity by ID / Obter Irregularidade Fiscal por ID"""
    item = db.query(IrregularidadeFiscal).filter(IrregularidadeFiscal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Irregularidade Fiscal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[IrregularidadeFiscalRead])
def listar_irregularidade_fiscal(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Tax Irregularity / Listar Irregularidade Fiscal"""
    return db.query(IrregularidadeFiscal).filter(
        IrregularidadeFiscal.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=IrregularidadeFiscalRead)
def atualizar_irregularidade_fiscal(
    item_id: int, 
    data: IrregularidadeFiscalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Tax Irregularity / Atualizar Irregularidade Fiscal"""
    item = db.query(IrregularidadeFiscal).filter(IrregularidadeFiscal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Irregularidade Fiscal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
