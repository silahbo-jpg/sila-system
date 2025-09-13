from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.loteamento_urbano import LoteamentoUrbano
from app.modules.urbanism.schemas.loteamento_urbano import LoteamentoUrbanoCreate, LoteamentoUrbanoRead, LoteamentoUrbanoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/loteamento-urbano", tags=["Loteamento Urbano"])

@router.post("/", response_model=LoteamentoUrbanoRead)
def criar_loteamento_urbano(
    data: LoteamentoUrbanoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Urban Subdivision / Criar novo Loteamento Urbano"""
    db_item = LoteamentoUrbano(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LoteamentoUrbanoRead)
def obter_loteamento_urbano(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Urban Subdivision by ID / Obter Loteamento Urbano por ID"""
    item = db.query(LoteamentoUrbano).filter(LoteamentoUrbano.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Loteamento Urbano não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[LoteamentoUrbanoRead])
def listar_loteamento_urbano(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Urban Subdivision / Listar Loteamento Urbano"""
    return db.query(LoteamentoUrbano).filter(
        LoteamentoUrbano.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=LoteamentoUrbanoRead)
def atualizar_loteamento_urbano(
    item_id: int, 
    data: LoteamentoUrbanoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Urban Subdivision / Atualizar Loteamento Urbano"""
    item = db.query(LoteamentoUrbano).filter(LoteamentoUrbano.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Loteamento Urbano não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
