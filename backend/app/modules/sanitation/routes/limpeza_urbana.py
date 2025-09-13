from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.limpeza_urbana import LimpezaUrbana
from app.modules.sanitation.schemas.limpeza_urbana import LimpezaUrbanaCreate, LimpezaUrbanaRead, LimpezaUrbanaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/limpeza-urbana", tags=["Limpeza Urbana"])

@router.post("/", response_model=LimpezaUrbanaRead)
def criar_limpeza_urbana(
    data: LimpezaUrbanaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Urban Cleaning / Criar novo Limpeza Urbana"""
    db_item = LimpezaUrbana(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LimpezaUrbanaRead)
def obter_limpeza_urbana(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Urban Cleaning by ID / Obter Limpeza Urbana por ID"""
    item = db.query(LimpezaUrbana).filter(LimpezaUrbana.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Limpeza Urbana não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[LimpezaUrbanaRead])
def listar_limpeza_urbana(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Urban Cleaning / Listar Limpeza Urbana"""
    return db.query(LimpezaUrbana).filter(
        LimpezaUrbana.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=LimpezaUrbanaRead)
def atualizar_limpeza_urbana(
    item_id: int, 
    data: LimpezaUrbanaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Urban Cleaning / Atualizar Limpeza Urbana"""
    item = db.query(LimpezaUrbana).filter(LimpezaUrbana.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Limpeza Urbana não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
