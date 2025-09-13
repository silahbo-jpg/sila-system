from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.registo_nascimento import RegistoNascimento
from app.modules.registry.schemas.registo_nascimento import RegistoNascimentoCreate, RegistoNascimentoRead, RegistoNascimentoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-nascimento", tags=["Registo de Nascimento"])

@router.post("/", response_model=RegistoNascimentoRead)
def criar_registo_nascimento(
    data: RegistoNascimentoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Birth Registration / Criar novo Registo de Nascimento"""
    db_item = RegistoNascimento(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoNascimentoRead)
def obter_registo_nascimento(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Birth Registration by ID / Obter Registo de Nascimento por ID"""
    item = db.query(RegistoNascimento).filter(RegistoNascimento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Nascimento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoNascimentoRead])
def listar_registo_nascimento(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Birth Registration / Listar Registo de Nascimento"""
    return db.query(RegistoNascimento).filter(
        RegistoNascimento.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoNascimentoRead)
def atualizar_registo_nascimento(
    item_id: int, 
    data: RegistoNascimentoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Birth Registration / Atualizar Registo de Nascimento"""
    item = db.query(RegistoNascimento).filter(RegistoNascimento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Nascimento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
