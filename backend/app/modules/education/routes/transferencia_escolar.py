from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.transferencia_escolar import TransferenciaEscolar
from app.modules.education.schemas.transferencia_escolar import TransferenciaEscolarCreate, TransferenciaEscolarRead, TransferenciaEscolarUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/transferencia-escolar", tags=["Transferência Escolar"])

@router.post("/", response_model=TransferenciaEscolarRead)
def criar_transferencia_escolar(
    data: TransferenciaEscolarCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new School Transfer / Criar novo Transferência Escolar"""
    db_item = TransferenciaEscolar(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=TransferenciaEscolarRead)
def obter_transferencia_escolar(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get School Transfer by ID / Obter Transferência Escolar por ID"""
    item = db.query(TransferenciaEscolar).filter(TransferenciaEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Transferência Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[TransferenciaEscolarRead])
def listar_transferencia_escolar(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List School Transfer / Listar Transferência Escolar"""
    return db.query(TransferenciaEscolar).filter(
        TransferenciaEscolar.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=TransferenciaEscolarRead)
def atualizar_transferencia_escolar(
    item_id: int, 
    data: TransferenciaEscolarUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update School Transfer / Atualizar Transferência Escolar"""
    item = db.query(TransferenciaEscolar).filter(TransferenciaEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Transferência Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
