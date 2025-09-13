from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.solicitacao_medicamento import SolicitacaoMedicamento
from app.modules.health.schemas.solicitacao_medicamento import SolicitacaoMedicamentoCreate, SolicitacaoMedicamentoRead, SolicitacaoMedicamentoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/solicitacao-medicamento", tags=["Solicitação de Medicamento"])

@router.post("/", response_model=SolicitacaoMedicamentoRead)
def criar_solicitacao_medicamento(
    data: SolicitacaoMedicamentoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Medication Request / Criar novo Solicitação de Medicamento"""
    db_item = SolicitacaoMedicamento(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SolicitacaoMedicamentoRead)
def obter_solicitacao_medicamento(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Medication Request by ID / Obter Solicitação de Medicamento por ID"""
    item = db.query(SolicitacaoMedicamento).filter(SolicitacaoMedicamento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Solicitação de Medicamento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SolicitacaoMedicamentoRead])
def listar_solicitacao_medicamento(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Medication Request / Listar Solicitação de Medicamento"""
    return db.query(SolicitacaoMedicamento).filter(
        SolicitacaoMedicamento.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SolicitacaoMedicamentoRead)
def atualizar_solicitacao_medicamento(
    item_id: int, 
    data: SolicitacaoMedicamentoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Medication Request / Atualizar Solicitação de Medicamento"""
    item = db.query(SolicitacaoMedicamento).filter(SolicitacaoMedicamento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Solicitação de Medicamento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
