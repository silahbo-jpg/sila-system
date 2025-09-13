from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.reclamacao_servico import ReclamacaoServico
from app.modules.complaints.schemas.reclamacao_servico import ReclamacaoServicoCreate, ReclamacaoServicoRead, ReclamacaoServicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/reclamacao-servico", tags=["Reclamação de Serviço"])

@router.post("/", response_model=ReclamacaoServicoRead)
def criar_reclamacao_servico(
    data: ReclamacaoServicoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Service Complaint / Criar novo Reclamação de Serviço"""
    db_item = ReclamacaoServico(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ReclamacaoServicoRead)
def obter_reclamacao_servico(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Service Complaint by ID / Obter Reclamação de Serviço por ID"""
    item = db.query(ReclamacaoServico).filter(ReclamacaoServico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reclamação de Serviço não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ReclamacaoServicoRead])
def listar_reclamacao_servico(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Service Complaint / Listar Reclamação de Serviço"""
    return db.query(ReclamacaoServico).filter(
        ReclamacaoServico.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ReclamacaoServicoRead)
def atualizar_reclamacao_servico(
    item_id: int, 
    data: ReclamacaoServicoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Service Complaint / Atualizar Reclamação de Serviço"""
    item = db.query(ReclamacaoServico).filter(ReclamacaoServico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reclamação de Serviço não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
