from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.educacao_ambiental import EducacaoAmbiental
from app.modules.sanitation.schemas.educacao_ambiental import EducacaoAmbientalCreate, EducacaoAmbientalRead, EducacaoAmbientalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/educacao-ambiental", tags=["Educação Ambiental"])

@router.post("/", response_model=EducacaoAmbientalRead)
def criar_educacao_ambiental(
    data: EducacaoAmbientalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Environmental Education / Criar novo Educação Ambiental"""
    db_item = EducacaoAmbiental(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EducacaoAmbientalRead)
def obter_educacao_ambiental(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Environmental Education by ID / Obter Educação Ambiental por ID"""
    item = db.query(EducacaoAmbiental).filter(EducacaoAmbiental.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Educação Ambiental não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EducacaoAmbientalRead])
def listar_educacao_ambiental(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Environmental Education / Listar Educação Ambiental"""
    return db.query(EducacaoAmbiental).filter(
        EducacaoAmbiental.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EducacaoAmbientalRead)
def atualizar_educacao_ambiental(
    item_id: int, 
    data: EducacaoAmbientalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Environmental Education / Atualizar Educação Ambiental"""
    item = db.query(EducacaoAmbiental).filter(EducacaoAmbiental.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Educação Ambiental não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
