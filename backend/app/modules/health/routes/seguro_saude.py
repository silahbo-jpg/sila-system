from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.seguro_saude import SeguroSaude
from app.modules.health.schemas.seguro_saude import SeguroSaudeCreate, SeguroSaudeRead, SeguroSaudeUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/seguro-saude", tags=["Seguro de Saúde Municipal"])

@router.post("/", response_model=SeguroSaudeRead)
def criar_seguro_saude(
    data: SeguroSaudeCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Health Insurance / Criar novo Seguro de Saúde Municipal"""
    db_item = SeguroSaude(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SeguroSaudeRead)
def obter_seguro_saude(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Health Insurance by ID / Obter Seguro de Saúde Municipal por ID"""
    item = db.query(SeguroSaude).filter(SeguroSaude.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Seguro de Saúde Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SeguroSaudeRead])
def listar_seguro_saude(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Health Insurance / Listar Seguro de Saúde Municipal"""
    return db.query(SeguroSaude).filter(
        SeguroSaude.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SeguroSaudeRead)
def atualizar_seguro_saude(
    item_id: int, 
    data: SeguroSaudeUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Health Insurance / Atualizar Seguro de Saúde Municipal"""
    item = db.query(SeguroSaude).filter(SeguroSaude.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Seguro de Saúde Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
