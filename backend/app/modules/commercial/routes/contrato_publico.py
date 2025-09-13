from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.contrato_publico import ContratoPublico
from app.modules.commercial.schemas.contrato_publico import ContratoPublicoCreate, ContratoPublicoRead, ContratoPublicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/contrato-publico", tags=["Contrato Público"])

@router.post("/", response_model=ContratoPublicoRead)
def criar_contrato_publico(
    data: ContratoPublicoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Public Contract / Criar novo Contrato Público"""
    db_item = ContratoPublico(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ContratoPublicoRead)
def obter_contrato_publico(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Public Contract by ID / Obter Contrato Público por ID"""
    item = db.query(ContratoPublico).filter(ContratoPublico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Contrato Público não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ContratoPublicoRead])
def listar_contrato_publico(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Public Contract / Listar Contrato Público"""
    return db.query(ContratoPublico).filter(
        ContratoPublico.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ContratoPublicoRead)
def atualizar_contrato_publico(
    item_id: int, 
    data: ContratoPublicoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Public Contract / Atualizar Contrato Público"""
    item = db.query(ContratoPublico).filter(ContratoPublico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Contrato Público não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
