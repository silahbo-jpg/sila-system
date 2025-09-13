from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.espaco_publico import EspacoPublico
from app.modules.urbanism.schemas.espaco_publico import EspacoPublicoCreate, EspacoPublicoRead, EspacoPublicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/espaco-publico", tags=["Uso de Espaço Público"])

@router.post("/", response_model=EspacoPublicoRead)
def criar_espaco_publico(
    data: EspacoPublicoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Public Space Usage / Criar novo Uso de Espaço Público"""
    db_item = EspacoPublico(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EspacoPublicoRead)
def obter_espaco_publico(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Public Space Usage by ID / Obter Uso de Espaço Público por ID"""
    item = db.query(EspacoPublico).filter(EspacoPublico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Uso de Espaço Público não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EspacoPublicoRead])
def listar_espaco_publico(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Public Space Usage / Listar Uso de Espaço Público"""
    return db.query(EspacoPublico).filter(
        EspacoPublico.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EspacoPublicoRead)
def atualizar_espaco_publico(
    item_id: int, 
    data: EspacoPublicoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Public Space Usage / Atualizar Uso de Espaço Público"""
    item = db.query(EspacoPublico).filter(EspacoPublico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Uso de Espaço Público não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
