from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.programa_idoso import ProgramaIdoso
from app.modules.social.schemas.programa_idoso import ProgramaIdosoCreate, ProgramaIdosoRead, ProgramaIdosoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/programa-idoso", tags=["Programa do Idoso"])

@router.post("/", response_model=ProgramaIdosoRead)
def criar_programa_idoso(
    data: ProgramaIdosoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Elderly Program / Criar novo Programa do Idoso"""
    db_item = ProgramaIdoso(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ProgramaIdosoRead)
def obter_programa_idoso(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Elderly Program by ID / Obter Programa do Idoso por ID"""
    item = db.query(ProgramaIdoso).filter(ProgramaIdoso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Programa do Idoso não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ProgramaIdosoRead])
def listar_programa_idoso(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Elderly Program / Listar Programa do Idoso"""
    return db.query(ProgramaIdoso).filter(
        ProgramaIdoso.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ProgramaIdosoRead)
def atualizar_programa_idoso(
    item_id: int, 
    data: ProgramaIdosoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Elderly Program / Atualizar Programa do Idoso"""
    item = db.query(ProgramaIdoso).filter(ProgramaIdoso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Programa do Idoso não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
