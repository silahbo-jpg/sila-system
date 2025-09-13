from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.leilao_judicial import LeilaoJudicial
from app.modules.justice.schemas.leilao_judicial import LeilaoJudicialCreate, LeilaoJudicialRead, LeilaoJudicialUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/leilao-judicial", tags=["Leilão Judicial"])

@router.post("/", response_model=LeilaoJudicialRead)
def criar_leilao_judicial(
    data: LeilaoJudicialCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Judicial Auction / Criar novo Leilão Judicial"""
    db_item = LeilaoJudicial(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LeilaoJudicialRead)
def obter_leilao_judicial(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Judicial Auction by ID / Obter Leilão Judicial por ID"""
    item = db.query(LeilaoJudicial).filter(LeilaoJudicial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Leilão Judicial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[LeilaoJudicialRead])
def listar_leilao_judicial(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Judicial Auction / Listar Leilão Judicial"""
    return db.query(LeilaoJudicial).filter(
        LeilaoJudicial.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=LeilaoJudicialRead)
def atualizar_leilao_judicial(
    item_id: int, 
    data: LeilaoJudicialUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Judicial Auction / Atualizar Leilão Judicial"""
    item = db.query(LeilaoJudicial).filter(LeilaoJudicial.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Leilão Judicial não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
