from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.transporte_escolar import TransporteEscolar
from app.modules.education.schemas.transporte_escolar import TransporteEscolarCreate, TransporteEscolarRead, TransporteEscolarUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/transporte-escolar", tags=["Transporte Escolar"])

@router.post("/", response_model=TransporteEscolarRead)
def criar_transporte_escolar(
    data: TransporteEscolarCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new School Transportation / Criar novo Transporte Escolar"""
    db_item = TransporteEscolar(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=TransporteEscolarRead)
def obter_transporte_escolar(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get School Transportation by ID / Obter Transporte Escolar por ID"""
    item = db.query(TransporteEscolar).filter(TransporteEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Transporte Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[TransporteEscolarRead])
def listar_transporte_escolar(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List School Transportation / Listar Transporte Escolar"""
    return db.query(TransporteEscolar).filter(
        TransporteEscolar.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=TransporteEscolarRead)
def atualizar_transporte_escolar(
    item_id: int, 
    data: TransporteEscolarUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update School Transportation / Atualizar Transporte Escolar"""
    item = db.query(TransporteEscolar).filter(TransporteEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Transporte Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
