from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.reconhecimento_paternidade import ReconhecimentoPaternidade
from app.modules.registry.schemas.reconhecimento_paternidade import ReconhecimentoPaternidadeCreate, ReconhecimentoPaternidadeRead, ReconhecimentoPaternidadeUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/reconhecimento-paternidade", tags=["Reconhecimento de Paternidade"])

@router.post("/", response_model=ReconhecimentoPaternidadeRead)
def criar_reconhecimento_paternidade(
    data: ReconhecimentoPaternidadeCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Paternity Recognition / Criar novo Reconhecimento de Paternidade"""
    db_item = ReconhecimentoPaternidade(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ReconhecimentoPaternidadeRead)
def obter_reconhecimento_paternidade(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Paternity Recognition by ID / Obter Reconhecimento de Paternidade por ID"""
    item = db.query(ReconhecimentoPaternidade).filter(ReconhecimentoPaternidade.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reconhecimento de Paternidade não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ReconhecimentoPaternidadeRead])
def listar_reconhecimento_paternidade(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Paternity Recognition / Listar Reconhecimento de Paternidade"""
    return db.query(ReconhecimentoPaternidade).filter(
        ReconhecimentoPaternidade.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ReconhecimentoPaternidadeRead)
def atualizar_reconhecimento_paternidade(
    item_id: int, 
    data: ReconhecimentoPaternidadeUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Paternity Recognition / Atualizar Reconhecimento de Paternidade"""
    item = db.query(ReconhecimentoPaternidade).filter(ReconhecimentoPaternidade.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Reconhecimento de Paternidade não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
