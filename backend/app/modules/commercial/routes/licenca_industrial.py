from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.licenca_industrial import LicencaIndustrial
from app.modules.commercial.schemas.licenca_industrial import LicencaIndustrialCreate, LicencaIndustrialRead, LicencaIndustrialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/licenca-industrial", tags=["Licença Industrial"])

@router.post("/", response_model=LicencaIndustrialRead)
def criar_licenca_industrial(
    data: LicencaIndustrialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Industrial License / Criar novo Licença Industrial"""
    db_item = LicencaIndustrial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LicencaIndustrialRead)
def obter_licenca_industrial(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Industrial License by ID / Obter Licença Industrial por ID"""
    item = db.query(LicencaIndustrial).filter(LicencaIndustrial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Licença Industrial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[LicencaIndustrialRead])
def listar_licenca_industrial(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Industrial License / Listar Licença Industrial"""
    return db.query(LicencaIndustrial).filter(
        LicencaIndustrial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=LicencaIndustrialRead)
def atualizar_licenca_industrial(
    item_id: int, 
    data: LicencaIndustrialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Industrial License / Atualizar Licença Industrial"""
    item = db.query(LicencaIndustrial).filter(LicencaIndustrial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Licença Industrial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
