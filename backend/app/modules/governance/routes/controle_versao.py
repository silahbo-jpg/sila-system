from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.governance.models.controle_versao import ControleVersao
from app.modules.governance.schemas.controle_versao import ControleVersaoCreate, ControleVersaoRead, ControleVersaoUpdate

router = APIRouter(prefix="/internal/controle-versao", tags=["Controle de Versão"])

@router.post("/", response_model=ControleVersaoRead)
def criar_controle_versao(data: ControleVersaoCreate):
    """Create new Version Control / Criar novo Controle de Versão"""
    db_item = ControleVersao(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ControleVersaoRead)
def obter_controle_versao(item_id: int):
    """Get Version Control by ID / Obter Controle de Versão por ID"""
    item = db.query(ControleVersao).filter(ControleVersao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de Versão não encontrado")
    return item

@router.get("/", response_model=List[ControleVersaoRead])
def listar_controle_versao(skip: int = 0, limit: int = 100):
    """List Version Control / Listar Controle de Versão"""
    return db.query(ControleVersao).offset(skip).limit(limit).all()

@router.put("/id", response_model=ControleVersaoRead)
def atualizar_controle_versao(item_id: int, data: ControleVersaoUpdate):
    """Update Version Control / Atualizar Controle de Versão"""
    item = db.query(ControleVersao).filter(ControleVersao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de Versão não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
