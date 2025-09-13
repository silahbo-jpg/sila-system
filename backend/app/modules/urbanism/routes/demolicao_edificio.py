from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.demolicao_edificio import DemolicaoEdificio
from app.modules.urbanism.schemas.demolicao_edificio import DemolicaoEdificioCreate, DemolicaoEdificioRead, DemolicaoEdificioUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/demolicao-edificio", tags=["Demolição de Edifício"])

@router.post("/", response_model=DemolicaoEdificioRead)
def criar_demolicao_edificio(
    data: DemolicaoEdificioCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Building Demolition / Criar novo Demolição de Edifício"""
    db_item = DemolicaoEdificio(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=DemolicaoEdificioRead)
def obter_demolicao_edificio(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Building Demolition by ID / Obter Demolição de Edifício por ID"""
    item = db.query(DemolicaoEdificio).filter(DemolicaoEdificio.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Demolição de Edifício não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[DemolicaoEdificioRead])
def listar_demolicao_edificio(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Building Demolition / Listar Demolição de Edifício"""
    return db.query(DemolicaoEdificio).filter(
        DemolicaoEdificio.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=DemolicaoEdificioRead)
def atualizar_demolicao_edificio(
    item_id: int, 
    data: DemolicaoEdificioUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Building Demolition / Atualizar Demolição de Edifício"""
    item = db.query(DemolicaoEdificio).filter(DemolicaoEdificio.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Demolição de Edifício não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
