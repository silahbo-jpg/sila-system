from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.regularizacao_fundiaria import RegularizacaoFundiaria
from app.modules.urbanism.schemas.regularizacao_fundiaria import RegularizacaoFundiariaCreate, RegularizacaoFundiariaRead, RegularizacaoFundiariaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/regularizacao-fundiaria", tags=["Regularização Fundiária"])

@router.post("/", response_model=RegularizacaoFundiariaRead)
def criar_regularizacao_fundiaria(
    data: RegularizacaoFundiariaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Land Regularization / Criar novo Regularização Fundiária"""
    db_item = RegularizacaoFundiaria(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegularizacaoFundiariaRead)
def obter_regularizacao_fundiaria(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Land Regularization by ID / Obter Regularização Fundiária por ID"""
    item = db.query(RegularizacaoFundiaria).filter(RegularizacaoFundiaria.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Regularização Fundiária não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegularizacaoFundiariaRead])
def listar_regularizacao_fundiaria(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Land Regularization / Listar Regularização Fundiária"""
    return db.query(RegularizacaoFundiaria).filter(
        RegularizacaoFundiaria.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegularizacaoFundiariaRead)
def atualizar_regularizacao_fundiaria(
    item_id: int, 
    data: RegularizacaoFundiariaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Land Regularization / Atualizar Regularização Fundiária"""
    item = db.query(RegularizacaoFundiaria).filter(RegularizacaoFundiaria.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Regularização Fundiária não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
