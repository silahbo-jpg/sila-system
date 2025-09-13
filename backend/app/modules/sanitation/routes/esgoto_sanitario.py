from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.esgoto_sanitario import EsgotoSanitario
from app.modules.sanitation.schemas.esgoto_sanitario import EsgotoSanitarioCreate, EsgotoSanitarioRead, EsgotoSanitarioUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/esgoto-sanitario", tags=["Esgoto Sanitário"])

@router.post("/", response_model=EsgotoSanitarioRead)
def criar_esgoto_sanitario(
    data: EsgotoSanitarioCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Sanitary Sewage / Criar novo Esgoto Sanitário"""
    db_item = EsgotoSanitario(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EsgotoSanitarioRead)
def obter_esgoto_sanitario(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Sanitary Sewage by ID / Obter Esgoto Sanitário por ID"""
    item = db.query(EsgotoSanitario).filter(EsgotoSanitario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Esgoto Sanitário não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EsgotoSanitarioRead])
def listar_esgoto_sanitario(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Sanitary Sewage / Listar Esgoto Sanitário"""
    return db.query(EsgotoSanitario).filter(
        EsgotoSanitario.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EsgotoSanitarioRead)
def atualizar_esgoto_sanitario(
    item_id: int, 
    data: EsgotoSanitarioUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Sanitary Sewage / Atualizar Esgoto Sanitário"""
    item = db.query(EsgotoSanitario).filter(EsgotoSanitario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Esgoto Sanitário não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
