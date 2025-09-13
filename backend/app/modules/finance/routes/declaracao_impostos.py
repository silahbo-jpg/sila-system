from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.declaracao_impostos import DeclaracaoImpostos
from app.modules.finance.schemas.declaracao_impostos import DeclaracaoImpostosCreate, DeclaracaoImpostosRead, DeclaracaoImpostosUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/declaracao-impostos", tags=["Declaração de Impostos"])

@router.post("/", response_model=DeclaracaoImpostosRead)
def criar_declaracao_impostos(
    data: DeclaracaoImpostosCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Tax Declaration / Criar novo Declaração de Impostos"""
    db_item = DeclaracaoImpostos(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=DeclaracaoImpostosRead)
def obter_declaracao_impostos(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Tax Declaration by ID / Obter Declaração de Impostos por ID"""
    item = db.query(DeclaracaoImpostos).filter(DeclaracaoImpostos.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Declaração de Impostos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[DeclaracaoImpostosRead])
def listar_declaracao_impostos(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Tax Declaration / Listar Declaração de Impostos"""
    return db.query(DeclaracaoImpostos).filter(
        DeclaracaoImpostos.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=DeclaracaoImpostosRead)
def atualizar_declaracao_impostos(
    item_id: int, 
    data: DeclaracaoImpostosUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Tax Declaration / Atualizar Declaração de Impostos"""
    item = db.query(DeclaracaoImpostos).filter(DeclaracaoImpostos.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Declaração de Impostos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
