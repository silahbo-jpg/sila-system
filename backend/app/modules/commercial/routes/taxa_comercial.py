from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.taxa_comercial import TaxaComercial
from app.modules.commercial.schemas.taxa_comercial import TaxaComercialCreate, TaxaComercialRead, TaxaComercialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/taxa-comercial", tags=["Taxa Comercial"])

@router.post("/", response_model=TaxaComercialRead)
def criar_taxa_comercial(
    data: TaxaComercialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Commercial Tax / Criar novo Taxa Comercial"""
    db_item = TaxaComercial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=TaxaComercialRead)
def obter_taxa_comercial(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Commercial Tax by ID / Obter Taxa Comercial por ID"""
    item = db.query(TaxaComercial).filter(TaxaComercial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Taxa Comercial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[TaxaComercialRead])
def listar_taxa_comercial(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Commercial Tax / Listar Taxa Comercial"""
    return db.query(TaxaComercial).filter(
        TaxaComercial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=TaxaComercialRead)
def atualizar_taxa_comercial(
    item_id: int, 
    data: TaxaComercialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Commercial Tax / Atualizar Taxa Comercial"""
    item = db.query(TaxaComercial).filter(TaxaComercial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Taxa Comercial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
