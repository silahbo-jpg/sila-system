from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.registo_obito import RegistoObito
from app.modules.registry.schemas.registo_obito import RegistoObitoCreate, RegistoObitoRead, RegistoObitoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-obito", tags=["Registo de Óbito"])

@router.post("/", response_model=RegistoObitoRead)
def criar_registo_obito(
    data: RegistoObitoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Death Registration / Criar novo Registo de Óbito"""
    db_item = RegistoObito(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoObitoRead)
def obter_registo_obito(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Death Registration by ID / Obter Registo de Óbito por ID"""
    item = db.query(RegistoObito).filter(RegistoObito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Óbito não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoObitoRead])
def listar_registo_obito(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Death Registration / Listar Registo de Óbito"""
    return db.query(RegistoObito).filter(
        RegistoObito.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoObitoRead)
def atualizar_registo_obito(
    item_id: int, 
    data: RegistoObitoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Death Registration / Atualizar Registo de Óbito"""
    item = db.query(RegistoObito).filter(RegistoObito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Óbito não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
