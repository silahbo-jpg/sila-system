from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.registo_casamento import RegistoCasamento
from app.modules.registry.schemas.registo_casamento import RegistoCasamentoCreate, RegistoCasamentoRead, RegistoCasamentoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-casamento", tags=["Registo de Casamento"])

@router.post("/", response_model=RegistoCasamentoRead)
def criar_registo_casamento(
    data: RegistoCasamentoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Marriage Registration / Criar novo Registo de Casamento"""
    db_item = RegistoCasamento(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoCasamentoRead)
def obter_registo_casamento(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Marriage Registration by ID / Obter Registo de Casamento por ID"""
    item = db.query(RegistoCasamento).filter(RegistoCasamento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Casamento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoCasamentoRead])
def listar_registo_casamento(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Marriage Registration / Listar Registo de Casamento"""
    return db.query(RegistoCasamento).filter(
        RegistoCasamento.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoCasamentoRead)
def atualizar_registo_casamento(
    item_id: int, 
    data: RegistoCasamentoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Marriage Registration / Atualizar Registo de Casamento"""
    item = db.query(RegistoCasamento).filter(RegistoCasamento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Casamento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
