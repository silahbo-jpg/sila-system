from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.tutela_menor import TutelaMenor
from app.modules.registry.schemas.tutela_menor import TutelaMenorCreate, TutelaMenorRead, TutelaMenorUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/tutela-menor", tags=["Tutela de Menor"])

@router.post("/", response_model=TutelaMenorRead)
def criar_tutela_menor(
    data: TutelaMenorCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Child Guardianship / Criar novo Tutela de Menor"""
    db_item = TutelaMenor(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=TutelaMenorRead)
def obter_tutela_menor(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Child Guardianship by ID / Obter Tutela de Menor por ID"""
    item = db.query(TutelaMenor).filter(TutelaMenor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tutela de Menor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[TutelaMenorRead])
def listar_tutela_menor(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Child Guardianship / Listar Tutela de Menor"""
    return db.query(TutelaMenor).filter(
        TutelaMenor.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=TutelaMenorRead)
def atualizar_tutela_menor(
    item_id: int, 
    data: TutelaMenorUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Child Guardianship / Atualizar Tutela de Menor"""
    item = db.query(TutelaMenor).filter(TutelaMenor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tutela de Menor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
