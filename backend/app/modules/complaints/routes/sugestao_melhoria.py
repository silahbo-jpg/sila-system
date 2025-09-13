from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.sugestao_melhoria import SugestaoMelhoria
from app.modules.complaints.schemas.sugestao_melhoria import SugestaoMelhoriaCreate, SugestaoMelhoriaRead, SugestaoMelhoriaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/sugestao-melhoria", tags=["Sugestão de Melhoria"])

@router.post("/", response_model=SugestaoMelhoriaRead)
def criar_sugestao_melhoria(
    data: SugestaoMelhoriaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Improvement Suggestion / Criar novo Sugestão de Melhoria"""
    db_item = SugestaoMelhoria(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SugestaoMelhoriaRead)
def obter_sugestao_melhoria(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Improvement Suggestion by ID / Obter Sugestão de Melhoria por ID"""
    item = db.query(SugestaoMelhoria).filter(SugestaoMelhoria.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sugestão de Melhoria não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SugestaoMelhoriaRead])
def listar_sugestao_melhoria(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Improvement Suggestion / Listar Sugestão de Melhoria"""
    return db.query(SugestaoMelhoria).filter(
        SugestaoMelhoria.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SugestaoMelhoriaRead)
def atualizar_sugestao_melhoria(
    item_id: int, 
    data: SugestaoMelhoriaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Improvement Suggestion / Atualizar Sugestão de Melhoria"""
    item = db.query(SugestaoMelhoria).filter(SugestaoMelhoria.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sugestão de Melhoria não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
