from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.alfabetizacao_adulto import AlfabetizacaoAdulto
from app.modules.education.schemas.alfabetizacao_adulto import AlfabetizacaoAdultoCreate, AlfabetizacaoAdultoRead, AlfabetizacaoAdultoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/alfabetizacao-adulto", tags=["Alfabetização de Adultos"])

@router.post("/", response_model=AlfabetizacaoAdultoRead)
def criar_alfabetizacao_adulto(
    data: AlfabetizacaoAdultoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Adult Literacy Program / Criar novo Alfabetização de Adultos"""
    db_item = AlfabetizacaoAdulto(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AlfabetizacaoAdultoRead)
def obter_alfabetizacao_adulto(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Adult Literacy Program by ID / Obter Alfabetização de Adultos por ID"""
    item = db.query(AlfabetizacaoAdulto).filter(AlfabetizacaoAdulto.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Alfabetização de Adultos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AlfabetizacaoAdultoRead])
def listar_alfabetizacao_adulto(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Adult Literacy Program / Listar Alfabetização de Adultos"""
    return db.query(AlfabetizacaoAdulto).filter(
        AlfabetizacaoAdulto.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AlfabetizacaoAdultoRead)
def atualizar_alfabetizacao_adulto(
    item_id: int, 
    data: AlfabetizacaoAdultoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Adult Literacy Program / Atualizar Alfabetização de Adultos"""
    item = db.query(AlfabetizacaoAdulto).filter(AlfabetizacaoAdulto.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Alfabetização de Adultos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
