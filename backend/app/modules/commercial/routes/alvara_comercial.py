from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.alvara_comercial import AlvaraComercial
from app.modules.commercial.schemas.alvara_comercial import AlvaraComercialCreate, AlvaraComercialRead, AlvaraComercialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/alvara-comercial", tags=["Alvará Comercial"])

@router.post("/", response_model=AlvaraComercialRead)
def criar_alvara_comercial(
    data: AlvaraComercialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Commercial License / Criar novo Alvará Comercial"""
    db_item = AlvaraComercial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AlvaraComercialRead)
def obter_alvara_comercial(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Commercial License by ID / Obter Alvará Comercial por ID"""
    item = db.query(AlvaraComercial).filter(AlvaraComercial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Alvará Comercial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AlvaraComercialRead])
def listar_alvara_comercial(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Commercial License / Listar Alvará Comercial"""
    return db.query(AlvaraComercial).filter(
        AlvaraComercial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AlvaraComercialRead)
def atualizar_alvara_comercial(
    item_id: int, 
    data: AlvaraComercialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Commercial License / Atualizar Alvará Comercial"""
    item = db.query(AlvaraComercial).filter(AlvaraComercial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Alvará Comercial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
