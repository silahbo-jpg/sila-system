from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.ocupacao_solo import OcupacaoSolo
from app.modules.urbanism.schemas.ocupacao_solo import OcupacaoSoloCreate, OcupacaoSoloRead, OcupacaoSoloUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/ocupacao-solo", tags=["Ocupação de Solo"])

@router.post("/", response_model=OcupacaoSoloRead)
def criar_ocupacao_solo(
    data: OcupacaoSoloCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Land Occupation / Criar novo Ocupação de Solo"""
    db_item = OcupacaoSolo(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=OcupacaoSoloRead)
def obter_ocupacao_solo(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Land Occupation by ID / Obter Ocupação de Solo por ID"""
    item = db.query(OcupacaoSolo).filter(OcupacaoSolo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ocupação de Solo não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[OcupacaoSoloRead])
def listar_ocupacao_solo(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Land Occupation / Listar Ocupação de Solo"""
    return db.query(OcupacaoSolo).filter(
        OcupacaoSolo.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=OcupacaoSoloRead)
def atualizar_ocupacao_solo(
    item_id: int, 
    data: OcupacaoSoloUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Land Occupation / Atualizar Ocupação de Solo"""
    item = db.query(OcupacaoSolo).filter(OcupacaoSolo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ocupação de Solo não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
