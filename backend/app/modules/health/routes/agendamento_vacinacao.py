from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.agendamento_vacinacao import AgendamentoVacinacao
from app.modules.health.schemas.agendamento_vacinacao import AgendamentoVacinacaoCreate, AgendamentoVacinacaoRead, AgendamentoVacinacaoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/agendamento-vacinacao", tags=["Agendamento de Vacinação"])

@router.post("/", response_model=AgendamentoVacinacaoRead)
def criar_agendamento_vacinacao(
    data: AgendamentoVacinacaoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Vaccination Scheduling / Criar novo Agendamento de Vacinação"""
    db_item = AgendamentoVacinacao(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AgendamentoVacinacaoRead)
def obter_agendamento_vacinacao(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Vaccination Scheduling by ID / Obter Agendamento de Vacinação por ID"""
    item = db.query(AgendamentoVacinacao).filter(AgendamentoVacinacao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento de Vacinação não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AgendamentoVacinacaoRead])
def listar_agendamento_vacinacao(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Vaccination Scheduling / Listar Agendamento de Vacinação"""
    return db.query(AgendamentoVacinacao).filter(
        AgendamentoVacinacao.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AgendamentoVacinacaoRead)
def atualizar_agendamento_vacinacao(
    item_id: int, 
    data: AgendamentoVacinacaoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Vaccination Scheduling / Atualizar Agendamento de Vacinação"""
    item = db.query(AgendamentoVacinacao).filter(AgendamentoVacinacao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento de Vacinação não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
