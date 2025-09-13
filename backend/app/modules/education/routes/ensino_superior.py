from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.ensino_superior import EnsinoSuperior
from app.modules.education.schemas.ensino_superior import EnsinoSuperiorCreate, EnsinoSuperiorRead, EnsinoSuperiorUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/ensino-superior", tags=["Apoio ao Ensino Superior"])

@router.post("/", response_model=EnsinoSuperiorRead)
def criar_ensino_superior(
    data: EnsinoSuperiorCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Higher Education Support / Criar novo Apoio ao Ensino Superior"""
    db_item = EnsinoSuperior(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EnsinoSuperiorRead)
def obter_ensino_superior(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Higher Education Support by ID / Obter Apoio ao Ensino Superior por ID"""
    item = db.query(EnsinoSuperior).filter(EnsinoSuperior.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Apoio ao Ensino Superior não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EnsinoSuperiorRead])
def listar_ensino_superior(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Higher Education Support / Listar Apoio ao Ensino Superior"""
    return db.query(EnsinoSuperior).filter(
        EnsinoSuperior.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EnsinoSuperiorRead)
def atualizar_ensino_superior(
    item_id: int, 
    data: EnsinoSuperiorUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Higher Education Support / Atualizar Apoio ao Ensino Superior"""
    item = db.query(EnsinoSuperior).filter(EnsinoSuperior.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Apoio ao Ensino Superior não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
