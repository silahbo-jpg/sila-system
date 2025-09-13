from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.registo_criminal import RegistoCriminal
from app.modules.justice.schemas.registo_criminal import RegistoCriminalCreate, RegistoCriminalRead, RegistoCriminalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-criminal", tags=["Registo Criminal"])

@router.post("/", response_model=RegistoCriminalRead)
def criar_registo_criminal(
    data: RegistoCriminalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Criminal Record / Criar novo Registo Criminal"""
    db_item = RegistoCriminal(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoCriminalRead)
def obter_registo_criminal(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Criminal Record by ID / Obter Registo Criminal por ID"""
    item = db.query(RegistoCriminal).filter(RegistoCriminal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo Criminal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoCriminalRead])
def listar_registo_criminal(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Criminal Record / Listar Registo Criminal"""
    return db.query(RegistoCriminal).filter(
        RegistoCriminal.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoCriminalRead)
def atualizar_registo_criminal(
    item_id: int, 
    data: RegistoCriminalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Criminal Record / Atualizar Registo Criminal"""
    item = db.query(RegistoCriminal).filter(RegistoCriminal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo Criminal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
