from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.inspecao_sanitaria import InspecaoSanitaria
from app.modules.commercial.schemas.inspecao_sanitaria import InspecaoSanitariaCreate, InspecaoSanitariaRead, InspecaoSanitariaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/inspecao-sanitaria", tags=["Inspeção Sanitária"])

@router.post("/", response_model=InspecaoSanitariaRead)
def criar_inspecao_sanitaria(
    data: InspecaoSanitariaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Sanitary Inspection / Criar novo Inspeção Sanitária"""
    db_item = InspecaoSanitaria(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=InspecaoSanitariaRead)
def obter_inspecao_sanitaria(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Sanitary Inspection by ID / Obter Inspeção Sanitária por ID"""
    item = db.query(InspecaoSanitaria).filter(InspecaoSanitaria.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inspeção Sanitária não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[InspecaoSanitariaRead])
def listar_inspecao_sanitaria(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Sanitary Inspection / Listar Inspeção Sanitária"""
    return db.query(InspecaoSanitaria).filter(
        InspecaoSanitaria.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=InspecaoSanitariaRead)
def atualizar_inspecao_sanitaria(
    item_id: int, 
    data: InspecaoSanitariaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Sanitary Inspection / Atualizar Inspeção Sanitária"""
    item = db.query(InspecaoSanitaria).filter(InspecaoSanitaria.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inspeção Sanitária não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
