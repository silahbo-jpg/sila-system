from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.subsidio_habitacao import SubsidioHabitacao
from app.modules.finance.schemas.subsidio_habitacao import SubsidioHabitacaoCreate, SubsidioHabitacaoRead, SubsidioHabitacaoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/subsidio-habitacao", tags=["Subsídio de Habitação"])

@router.post("/", response_model=SubsidioHabitacaoRead)
def criar_subsidio_habitacao(
    data: SubsidioHabitacaoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Housing Subsidy / Criar novo Subsídio de Habitação"""
    db_item = SubsidioHabitacao(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SubsidioHabitacaoRead)
def obter_subsidio_habitacao(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Housing Subsidy by ID / Obter Subsídio de Habitação por ID"""
    item = db.query(SubsidioHabitacao).filter(SubsidioHabitacao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Subsídio de Habitação não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SubsidioHabitacaoRead])
def listar_subsidio_habitacao(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Housing Subsidy / Listar Subsídio de Habitação"""
    return db.query(SubsidioHabitacao).filter(
        SubsidioHabitacao.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SubsidioHabitacaoRead)
def atualizar_subsidio_habitacao(
    item_id: int, 
    data: SubsidioHabitacaoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Housing Subsidy / Atualizar Subsídio de Habitação"""
    item = db.query(SubsidioHabitacao).filter(SubsidioHabitacao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Subsídio de Habitação não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
