from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.fiscalizacao_obra import FiscalizacaoObra
from app.modules.complaints.schemas.fiscalizacao_obra import FiscalizacaoObraCreate, FiscalizacaoObraRead, FiscalizacaoObraUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/fiscalizacao-obra", tags=["Fiscalização de Obra"])

@router.post("/", response_model=FiscalizacaoObraRead)
def criar_fiscalizacao_obra(
    data: FiscalizacaoObraCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Construction Oversight / Criar novo Fiscalização de Obra"""
    db_item = FiscalizacaoObra(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=FiscalizacaoObraRead)
def obter_fiscalizacao_obra(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Construction Oversight by ID / Obter Fiscalização de Obra por ID"""
    item = db.query(FiscalizacaoObra).filter(FiscalizacaoObra.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Fiscalização de Obra não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[FiscalizacaoObraRead])
def listar_fiscalizacao_obra(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Construction Oversight / Listar Fiscalização de Obra"""
    return db.query(FiscalizacaoObra).filter(
        FiscalizacaoObra.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=FiscalizacaoObraRead)
def atualizar_fiscalizacao_obra(
    item_id: int, 
    data: FiscalizacaoObraUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Construction Oversight / Atualizar Fiscalização de Obra"""
    item = db.query(FiscalizacaoObra).filter(FiscalizacaoObra.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Fiscalização de Obra não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
