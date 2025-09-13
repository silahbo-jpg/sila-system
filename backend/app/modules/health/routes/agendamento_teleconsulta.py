from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.health.models.agendamento_teleconsulta import AgendamentoTeleconsulta
from app.modules.health.schemas.agendamento_teleconsulta import AgendamentoTeleconsultaCreate, AgendamentoTeleconsultaRead, AgendamentoTeleconsultaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/agendamento-teleconsulta", tags=["Agendamento Teleconsulta"])

@router.post("/", response_model=AgendamentoTeleconsultaRead)
def criar_agendamento_teleconsulta(
    data: AgendamentoTeleconsultaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    db_item = AgendamentoTeleconsulta(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AgendamentoTeleconsultaRead)
def obter_agendamento_teleconsulta(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    item = db.query(AgendamentoTeleconsulta).filter(AgendamentoTeleconsulta.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento Teleconsulta não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=list[AgendamentoTeleconsultaRead])
def listar_agendamento_teleconsulta(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return db.query(AgendamentoTeleconsulta).filter(AgendamentoTeleconsulta.municipe_id == current_user.id).offset(skip).limit(limit).all()

@router.put("/id", response_model=AgendamentoTeleconsultaRead)
def atualizar_agendamento_teleconsulta(
    item_id: int,
    data: AgendamentoTeleconsultaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    item = db.query(AgendamentoTeleconsulta).filter(AgendamentoTeleconsulta.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agendamento Teleconsulta não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

