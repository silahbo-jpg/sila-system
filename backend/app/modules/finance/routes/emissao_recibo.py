from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.emissao_recibo import EmissaoRecibo
from app.modules.finance.schemas.emissao_recibo import EmissaoReciboCreate, EmissaoReciboRead, EmissaoReciboUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/emissao-recibo", tags=["Emissão de Recibo"])

@router.post("/", response_model=EmissaoReciboRead)
def criar_emissao_recibo(
    data: EmissaoReciboCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Receipt Issuance / Criar novo Emissão de Recibo"""
    db_item = EmissaoRecibo(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EmissaoReciboRead)
def obter_emissao_recibo(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Receipt Issuance by ID / Obter Emissão de Recibo por ID"""
    item = db.query(EmissaoRecibo).filter(EmissaoRecibo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Emissão de Recibo não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EmissaoReciboRead])
def listar_emissao_recibo(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Receipt Issuance / Listar Emissão de Recibo"""
    return db.query(EmissaoRecibo).filter(
        EmissaoRecibo.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EmissaoReciboRead)
def atualizar_emissao_recibo(
    item_id: int, 
    data: EmissaoReciboUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Receipt Issuance / Atualizar Emissão de Recibo"""
    item = db.query(EmissaoRecibo).filter(EmissaoRecibo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Emissão de Recibo não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
