from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.execucao_fiscal import ExecucaoFiscal
from app.modules.justice.schemas.execucao_fiscal import ExecucaoFiscalCreate, ExecucaoFiscalRead, ExecucaoFiscalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/execucao-fiscal", tags=["Execução Fiscal"])

@router.post("/", response_model=ExecucaoFiscalRead)
def criar_execucao_fiscal(
    data: ExecucaoFiscalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Tax Execution / Criar novo Execução Fiscal"""
    db_item = ExecucaoFiscal(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ExecucaoFiscalRead)
def obter_execucao_fiscal(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Tax Execution by ID / Obter Execução Fiscal por ID"""
    item = db.query(ExecucaoFiscal).filter(ExecucaoFiscal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Execução Fiscal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ExecucaoFiscalRead])
def listar_execucao_fiscal(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Tax Execution / Listar Execução Fiscal"""
    return db.query(ExecucaoFiscal).filter(
        ExecucaoFiscal.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ExecucaoFiscalRead)
def atualizar_execucao_fiscal(
    item_id: int, 
    data: ExecucaoFiscalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Tax Execution / Atualizar Execução Fiscal"""
    item = db.query(ExecucaoFiscal).filter(ExecucaoFiscal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Execução Fiscal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
