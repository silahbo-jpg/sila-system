from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.ouvidoria_municipal import OuvidoriaMunicipal
from app.modules.complaints.schemas.ouvidoria_municipal import OuvidoriaMunicipalCreate, OuvidoriaMunicipalRead, OuvidoriaMunicipalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/ouvidoria-municipal", tags=["Ouvidoria Municipal"])

@router.post("/", response_model=OuvidoriaMunicipalRead)
def criar_ouvidoria_municipal(
    data: OuvidoriaMunicipalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Ombudsman / Criar novo Ouvidoria Municipal"""
    db_item = OuvidoriaMunicipal(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=OuvidoriaMunicipalRead)
def obter_ouvidoria_municipal(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Ombudsman by ID / Obter Ouvidoria Municipal por ID"""
    item = db.query(OuvidoriaMunicipal).filter(OuvidoriaMunicipal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ouvidoria Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[OuvidoriaMunicipalRead])
def listar_ouvidoria_municipal(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Ombudsman / Listar Ouvidoria Municipal"""
    return db.query(OuvidoriaMunicipal).filter(
        OuvidoriaMunicipal.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=OuvidoriaMunicipalRead)
def atualizar_ouvidoria_municipal(
    item_id: int, 
    data: OuvidoriaMunicipalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Ombudsman / Atualizar Ouvidoria Municipal"""
    item = db.query(OuvidoriaMunicipal).filter(OuvidoriaMunicipal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ouvidoria Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
