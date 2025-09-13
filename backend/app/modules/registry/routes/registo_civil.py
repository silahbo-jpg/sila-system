from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.registo_civil import RegistoCivil
from app.modules.registry.schemas.registo_civil import RegistoCivilCreate, RegistoCivilRead, RegistoCivilUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-civil", tags=["Registo Civil"])

@router.post("/", response_model=RegistoCivilRead)
def criar_registo_civil(
    data: RegistoCivilCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Civil Registry / Criar novo Registo Civil"""
    db_item = RegistoCivil(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoCivilRead)
def obter_registo_civil(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Civil Registry by ID / Obter Registo Civil por ID"""
    item = db.query(RegistoCivil).filter(RegistoCivil.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo Civil não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoCivilRead])
def listar_registo_civil(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Civil Registry / Listar Registo Civil"""
    return db.query(RegistoCivil).filter(
        RegistoCivil.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoCivilRead)
def atualizar_registo_civil(
    item_id: int, 
    data: RegistoCivilUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Civil Registry / Atualizar Registo Civil"""
    item = db.query(RegistoCivil).filter(RegistoCivil.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo Civil não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
