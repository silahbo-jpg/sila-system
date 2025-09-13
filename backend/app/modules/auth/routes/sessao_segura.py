from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.auth.models.sessao_segura import SessaoSegura
from app.modules.auth.schemas.sessao_segura import SessaoSeguraCreate, SessaoSeguraRead, SessaoSeguraUpdate

router = APIRouter(prefix="/internal/sessao-segura", tags=["Sessão Segura"])

@router.post("/", response_model=SessaoSeguraRead)
def criar_sessao_segura(data: SessaoSeguraCreate):
    """Create new Secure Session / Criar novo Sessão Segura"""
    db_item = SessaoSegura(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SessaoSeguraRead)
def obter_sessao_segura(item_id: int):
    """Get Secure Session by ID / Obter Sessão Segura por ID"""
    item = db.query(SessaoSegura).filter(SessaoSegura.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sessão Segura não encontrado")
    return item

@router.get("/", response_model=List[SessaoSeguraRead])
def listar_sessao_segura(skip: int = 0, limit: int = 100):
    """List Secure Session / Listar Sessão Segura"""
    return db.query(SessaoSegura).offset(skip).limit(limit).all()

@router.put("/id", response_model=SessaoSeguraRead)
def atualizar_sessao_segura(item_id: int, data: SessaoSeguraUpdate):
    """Update Secure Session / Atualizar Sessão Segura"""
    item = db.query(SessaoSegura).filter(SessaoSegura.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sessão Segura não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
