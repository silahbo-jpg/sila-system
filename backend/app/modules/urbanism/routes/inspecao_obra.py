from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.inspecao_obra import InspecaoObra
from app.modules.urbanism.schemas.inspecao_obra import InspecaoObraCreate, InspecaoObraRead, InspecaoObraUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/inspecao-obra", tags=["Inspeção de Obra"])

@router.post("/", response_model=InspecaoObraRead)
def criar_inspecao_obra(
    data: InspecaoObraCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Construction Inspection / Criar novo Inspeção de Obra"""
    db_item = InspecaoObra(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=InspecaoObraRead)
def obter_inspecao_obra(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Construction Inspection by ID / Obter Inspeção de Obra por ID"""
    item = db.query(InspecaoObra).filter(InspecaoObra.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inspeção de Obra não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[InspecaoObraRead])
def listar_inspecao_obra(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Construction Inspection / Listar Inspeção de Obra"""
    return db.query(InspecaoObra).filter(
        InspecaoObra.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=InspecaoObraRead)
def atualizar_inspecao_obra(
    item_id: int, 
    data: InspecaoObraUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Construction Inspection / Atualizar Inspeção de Obra"""
    item = db.query(InspecaoObra).filter(InspecaoObra.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inspeção de Obra não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
