from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.controle_vetores import ControleVetores
from app.modules.sanitation.schemas.controle_vetores import ControleVetoresCreate, ControleVetoresRead, ControleVetoresUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/controle-vetores", tags=["Controle de Vetores"])

@router.post("/", response_model=ControleVetoresRead)
def criar_controle_vetores(
    data: ControleVetoresCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Vector Control / Criar novo Controle de Vetores"""
    db_item = ControleVetores(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ControleVetoresRead)
def obter_controle_vetores(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Vector Control by ID / Obter Controle de Vetores por ID"""
    item = db.query(ControleVetores).filter(ControleVetores.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de Vetores não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ControleVetoresRead])
def listar_controle_vetores(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Vector Control / Listar Controle de Vetores"""
    return db.query(ControleVetores).filter(
        ControleVetores.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ControleVetoresRead)
def atualizar_controle_vetores(
    item_id: int, 
    data: ControleVetoresUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Vector Control / Atualizar Controle de Vetores"""
    item = db.query(ControleVetores).filter(ControleVetores.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de Vetores não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
