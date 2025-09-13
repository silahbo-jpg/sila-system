from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.capacitacao_profissional import CapacitacaoProfissional
from app.modules.social.schemas.capacitacao_profissional import CapacitacaoProfissionalCreate, CapacitacaoProfissionalRead, CapacitacaoProfissionalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/capacitacao-profissional", tags=["Capacitação Profissional"])

@router.post("/", response_model=CapacitacaoProfissionalRead)
def criar_capacitacao_profissional(
    data: CapacitacaoProfissionalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Professional Training / Criar novo Capacitação Profissional"""
    db_item = CapacitacaoProfissional(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CapacitacaoProfissionalRead)
def obter_capacitacao_profissional(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Professional Training by ID / Obter Capacitação Profissional por ID"""
    item = db.query(CapacitacaoProfissional).filter(CapacitacaoProfissional.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Capacitação Profissional não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CapacitacaoProfissionalRead])
def listar_capacitacao_profissional(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Professional Training / Listar Capacitação Profissional"""
    return db.query(CapacitacaoProfissional).filter(
        CapacitacaoProfissional.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CapacitacaoProfissionalRead)
def atualizar_capacitacao_profissional(
    item_id: int, 
    data: CapacitacaoProfissionalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Professional Training / Atualizar Capacitação Profissional"""
    item = db.query(CapacitacaoProfissional).filter(CapacitacaoProfissional.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Capacitação Profissional não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
