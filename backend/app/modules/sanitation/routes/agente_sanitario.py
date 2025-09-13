from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.sanitation.models.agente_sanitario import AgenteSanitario
from app.modules.sanitation.schemas.agente_sanitario import AgenteSanitarioCreate, AgenteSanitarioRead, AgenteSanitarioUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/agente-sanitario", tags=["Agente Sanitário"])

@router.post("/", response_model=AgenteSanitarioRead)
def criar_agente_sanitario(
    data: AgenteSanitarioCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Sanitary Agent / Criar novo Agente Sanitário"""
    db_item = AgenteSanitario(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AgenteSanitarioRead)
def obter_agente_sanitario(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Sanitary Agent by ID / Obter Agente Sanitário por ID"""
    item = db.query(AgenteSanitario).filter(AgenteSanitario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agente Sanitário não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AgenteSanitarioRead])
def listar_agente_sanitario(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Sanitary Agent / Listar Agente Sanitário"""
    return db.query(AgenteSanitario).filter(
        AgenteSanitario.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AgenteSanitarioRead)
def atualizar_agente_sanitario(
    item_id: int, 
    data: AgenteSanitarioUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Sanitary Agent / Atualizar Agente Sanitário"""
    item = db.query(AgenteSanitario).filter(AgenteSanitario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Agente Sanitário não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
