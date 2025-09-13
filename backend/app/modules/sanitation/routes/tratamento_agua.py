from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.tratamento_agua import TratamentoAgua
from app.modules.sanitation.schemas.tratamento_agua import TratamentoAguaCreate, TratamentoAguaRead, TratamentoAguaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/tratamento-agua", tags=["Tratamento de Água"])

@router.post("/", response_model=TratamentoAguaRead)
def criar_tratamento_agua(
    data: TratamentoAguaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Water Treatment / Criar novo Tratamento de Água"""
    db_item = TratamentoAgua(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=TratamentoAguaRead)
def obter_tratamento_agua(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Water Treatment by ID / Obter Tratamento de Água por ID"""
    item = db.query(TratamentoAgua).filter(TratamentoAgua.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tratamento de Água não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[TratamentoAguaRead])
def listar_tratamento_agua(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Water Treatment / Listar Tratamento de Água"""
    return db.query(TratamentoAgua).filter(
        TratamentoAgua.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=TratamentoAguaRead)
def atualizar_tratamento_agua(
    item_id: int, 
    data: TratamentoAguaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Water Treatment / Atualizar Tratamento de Água"""
    item = db.query(TratamentoAgua).filter(TratamentoAgua.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tratamento de Água não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
