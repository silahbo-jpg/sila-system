from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.auth.models.controle_acesso import ControleAcesso
from app.modules.auth.schemas.controle_acesso import ControleAcessoCreate, ControleAcessoRead, ControleAcessoUpdate

router = APIRouter(prefix="/internal/controle-acesso", tags=["Controle de Acesso"])

@router.post("/", response_model=ControleAcessoRead)
def criar_controle_acesso(data: ControleAcessoCreate):
    """Create new Access Control / Criar novo Controle de Acesso"""
    db_item = ControleAcesso(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ControleAcessoRead)
def obter_controle_acesso(item_id: int):
    """Get Access Control by ID / Obter Controle de Acesso por ID"""
    item = db.query(ControleAcesso).filter(ControleAcesso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de Acesso não encontrado")
    return item

@router.get("/", response_model=List[ControleAcessoRead])
def listar_controle_acesso(skip: int = 0, limit: int = 100):
    """List Access Control / Listar Controle de Acesso"""
    return db.query(ControleAcesso).offset(skip).limit(limit).all()

@router.put("/id", response_model=ControleAcessoRead)
def atualizar_controle_acesso(item_id: int, data: ControleAcessoUpdate):
    """Update Access Control / Atualizar Controle de Acesso"""
    item = db.query(ControleAcesso).filter(ControleAcesso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de Acesso não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
