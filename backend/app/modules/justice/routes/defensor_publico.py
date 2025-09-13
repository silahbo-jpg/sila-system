from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.defensor_publico import DefensorPublico
from app.modules.justice.schemas.defensor_publico import DefensorPublicoCreate, DefensorPublicoRead, DefensorPublicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/defensor-publico", tags=["Defensor Público"])

@router.post("/", response_model=DefensorPublicoRead)
def criar_defensor_publico(
    data: DefensorPublicoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Public Defender / Criar novo Defensor Público"""
    db_item = DefensorPublico(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=DefensorPublicoRead)
def obter_defensor_publico(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Public Defender by ID / Obter Defensor Público por ID"""
    item = db.query(DefensorPublico).filter(DefensorPublico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Defensor Público não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[DefensorPublicoRead])
def listar_defensor_publico(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Public Defender / Listar Defensor Público"""
    return db.query(DefensorPublico).filter(
        DefensorPublico.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=DefensorPublicoRead)
def atualizar_defensor_publico(
    item_id: int, 
    data: DefensorPublicoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Public Defender / Atualizar Defensor Público"""
    item = db.query(DefensorPublico).filter(DefensorPublico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Defensor Público não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
