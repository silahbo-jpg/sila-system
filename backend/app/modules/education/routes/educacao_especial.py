from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.educacao_especial import EducacaoEspecial
from app.modules.education.schemas.educacao_especial import EducacaoEspecialCreate, EducacaoEspecialRead, EducacaoEspecialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/educacao-especial", tags=["Educação Especial"])

@router.post("/", response_model=EducacaoEspecialRead)
def criar_educacao_especial(
    data: EducacaoEspecialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Special Education / Criar novo Educação Especial"""
    db_item = EducacaoEspecial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EducacaoEspecialRead)
def obter_educacao_especial(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Special Education by ID / Obter Educação Especial por ID"""
    item = db.query(EducacaoEspecial).filter(EducacaoEspecial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Educação Especial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EducacaoEspecialRead])
def listar_educacao_especial(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Special Education / Listar Educação Especial"""
    return db.query(EducacaoEspecial).filter(
        EducacaoEspecial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EducacaoEspecialRead)
def atualizar_educacao_especial(
    item_id: int, 
    data: EducacaoEspecialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Special Education / Atualizar Educação Especial"""
    item = db.query(EducacaoEspecial).filter(EducacaoEspecial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Educação Especial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
