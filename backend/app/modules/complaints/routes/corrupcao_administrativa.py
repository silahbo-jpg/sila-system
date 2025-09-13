from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.corrupcao_administrativa import CorrupcaoAdministrativa
from app.modules.complaints.schemas.corrupcao_administrativa import CorrupcaoAdministrativaCreate, CorrupcaoAdministrativaRead, CorrupcaoAdministrativaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/corrupcao-administrativa", tags=["Corrupção Administrativa"])

@router.post("/", response_model=CorrupcaoAdministrativaRead)
def criar_corrupcao_administrativa(
    data: CorrupcaoAdministrativaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Administrative Corruption / Criar novo Corrupção Administrativa"""
    db_item = CorrupcaoAdministrativa(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CorrupcaoAdministrativaRead)
def obter_corrupcao_administrativa(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Administrative Corruption by ID / Obter Corrupção Administrativa por ID"""
    item = db.query(CorrupcaoAdministrativa).filter(CorrupcaoAdministrativa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Corrupção Administrativa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CorrupcaoAdministrativaRead])
def listar_corrupcao_administrativa(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Administrative Corruption / Listar Corrupção Administrativa"""
    return db.query(CorrupcaoAdministrativa).filter(
        CorrupcaoAdministrativa.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CorrupcaoAdministrativaRead)
def atualizar_corrupcao_administrativa(
    item_id: int, 
    data: CorrupcaoAdministrativaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Administrative Corruption / Atualizar Corrupção Administrativa"""
    item = db.query(CorrupcaoAdministrativa).filter(CorrupcaoAdministrativa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Corrupção Administrativa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
