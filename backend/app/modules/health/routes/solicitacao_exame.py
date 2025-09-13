from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.solicitacao_exame import SolicitacaoExame
from app.modules.health.schemas.solicitacao_exame import SolicitacaoExameCreate, SolicitacaoExameRead, SolicitacaoExameUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/solicitacao-exame", tags=["Solicitação de Exame Laboratorial"])

@router.post("/", response_model=SolicitacaoExameRead)
def criar_solicitacao_exame(
    data: SolicitacaoExameCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Laboratory Test Request / Criar novo Solicitação de Exame Laboratorial"""
    db_item = SolicitacaoExame(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SolicitacaoExameRead)
def obter_solicitacao_exame(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Laboratory Test Request by ID / Obter Solicitação de Exame Laboratorial por ID"""
    item = db.query(SolicitacaoExame).filter(SolicitacaoExame.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Solicitação de Exame Laboratorial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SolicitacaoExameRead])
def listar_solicitacao_exame(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Laboratory Test Request / Listar Solicitação de Exame Laboratorial"""
    return db.query(SolicitacaoExame).filter(
        SolicitacaoExame.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SolicitacaoExameRead)
def atualizar_solicitacao_exame(
    item_id: int, 
    data: SolicitacaoExameUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Laboratory Test Request / Atualizar Solicitação de Exame Laboratorial"""
    item = db.query(SolicitacaoExame).filter(SolicitacaoExame.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Solicitação de Exame Laboratorial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
