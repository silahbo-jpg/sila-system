from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.auth.models.autenticacao_multifator import AutenticacaoMultifator
from app.modules.auth.schemas.autenticacao_multifator import AutenticacaoMultifatorCreate, AutenticacaoMultifatorRead, AutenticacaoMultifatorUpdate

router = APIRouter(prefix="/internal/autenticacao-multifator", tags=["Autenticação Multifator"])

@router.post("/", response_model=AutenticacaoMultifatorRead)
def criar_autenticacao_multifator(data: AutenticacaoMultifatorCreate):
    """Create new Multi-factor Authentication / Criar novo Autenticação Multifator"""
    db_item = AutenticacaoMultifator(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AutenticacaoMultifatorRead)
def obter_autenticacao_multifator(item_id: int):
    """Get Multi-factor Authentication by ID / Obter Autenticação Multifator por ID"""
    item = db.query(AutenticacaoMultifator).filter(AutenticacaoMultifator.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Autenticação Multifator não encontrado")
    return item

@router.get("/", response_model=List[AutenticacaoMultifatorRead])
def listar_autenticacao_multifator(skip: int = 0, limit: int = 100):
    """List Multi-factor Authentication / Listar Autenticação Multifator"""
    return db.query(AutenticacaoMultifator).offset(skip).limit(limit).all()

@router.put("/id", response_model=AutenticacaoMultifatorRead)
def atualizar_autenticacao_multifator(item_id: int, data: AutenticacaoMultifatorUpdate):
    """Update Multi-factor Authentication / Atualizar Autenticação Multifator"""
    item = db.query(AutenticacaoMultifator).filter(AutenticacaoMultifator.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Autenticação Multifator não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
