from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.isencao_taxa import IsencaoTaxa
from app.modules.finance.schemas.isencao_taxa import IsencaoTaxaCreate, IsencaoTaxaRead, IsencaoTaxaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/isencao-taxa", tags=["Isenção de Taxa"])

@router.post("/", response_model=IsencaoTaxaRead)
def criar_isencao_taxa(
    data: IsencaoTaxaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Tax Exemption / Criar novo Isenção de Taxa"""
    db_item = IsencaoTaxa(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=IsencaoTaxaRead)
def obter_isencao_taxa(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Tax Exemption by ID / Obter Isenção de Taxa por ID"""
    item = db.query(IsencaoTaxa).filter(IsencaoTaxa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Isenção de Taxa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[IsencaoTaxaRead])
def listar_isencao_taxa(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Tax Exemption / Listar Isenção de Taxa"""
    return db.query(IsencaoTaxa).filter(
        IsencaoTaxa.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=IsencaoTaxaRead)
def atualizar_isencao_taxa(
    item_id: int, 
    data: IsencaoTaxaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Tax Exemption / Atualizar Isenção de Taxa"""
    item = db.query(IsencaoTaxa).filter(IsencaoTaxa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Isenção de Taxa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
