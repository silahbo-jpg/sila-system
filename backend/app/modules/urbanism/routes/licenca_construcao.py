from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.licenca_construcao import LicencaConstrucao
from app.modules.urbanism.schemas.licenca_construcao import LicencaConstrucaoCreate, LicencaConstrucaoRead, LicencaConstrucaoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/licenca-construcao", tags=["Licença de Construção"])

@router.post("/", response_model=LicencaConstrucaoRead)
def criar_licenca_construcao(
    data: LicencaConstrucaoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Construction License / Criar novo Licença de Construção"""
    db_item = LicencaConstrucao(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LicencaConstrucaoRead)
def obter_licenca_construcao(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Construction License by ID / Obter Licença de Construção por ID"""
    item = db.query(LicencaConstrucao).filter(LicencaConstrucao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Licença de Construção não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[LicencaConstrucaoRead])
def listar_licenca_construcao(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Construction License / Listar Licença de Construção"""
    return db.query(LicencaConstrucao).filter(
        LicencaConstrucao.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=LicencaConstrucaoRead)
def atualizar_licenca_construcao(
    item_id: int, 
    data: LicencaConstrucaoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Construction License / Atualizar Licença de Construção"""
    item = db.query(LicencaConstrucao).filter(LicencaConstrucao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Licença de Construção não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
