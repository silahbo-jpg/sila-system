from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.agendamento_consulta import AgendamentoConsulta
from app.modules.health.schemas.agendamento_consulta import AgendamentoConsultaCreate, AgendamentoConsultaRead, AgendamentoConsultaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/agendamento-consulta", tags=["Agendamento de Consulta Médica"])

@router.post("/", response_model=AgendamentoConsultaRead)
def criar_agendamento_consulta(
    data: AgendamentoConsultaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Medical Appointment Booking / Criar novo Agendamento de Consulta Médica"""
    db_item = AgendamentoConsulta(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AgendamentoConsultaRead)
def obter_agendamento_consulta(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Medical Appointment Booking by ID / Obter Agendamento de Consulta Médica por ID"""
    item = db.query(AgendamentoConsulta).filter(AgendamentoConsulta.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento de Consulta Médica não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AgendamentoConsultaRead])
def listar_agendamento_consulta(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Medical Appointment Booking / Listar Agendamento de Consulta Médica"""
    return db.query(AgendamentoConsulta).filter(
        AgendamentoConsulta.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AgendamentoConsultaRead)
def atualizar_agendamento_consulta(
    item_id: int, 
    data: AgendamentoConsultaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Medical Appointment Booking / Atualizar Agendamento de Consulta Médica"""
    item = db.query(AgendamentoConsulta).filter(AgendamentoConsulta.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento de Consulta Médica não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
