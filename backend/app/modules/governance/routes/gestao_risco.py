from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.governance.models.gestao_risco import GestaoRisco
from app.modules.governance.schemas.gestao_risco import GestaoRiscoCreate, GestaoRiscoRead, GestaoRiscoUpdate

router = APIRouter(prefix="/internal/gestao-risco", tags=["Gestão de Risco"])

@router.post("/", response_model=GestaoRiscoRead)
def criar_gestao_risco(data: GestaoRiscoCreate):
    """Create new Risk Management / Criar novo Gestão de Risco"""
    db_item = GestaoRisco(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=GestaoRiscoRead)
def obter_gestao_risco(item_id: int):
    """Get Risk Management by ID / Obter Gestão de Risco por ID"""
    item = db.query(GestaoRisco).filter(GestaoRisco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gestão de Risco não encontrado")
    return item

@router.get("/", response_model=List[GestaoRiscoRead])
def listar_gestao_risco(skip: int = 0, limit: int = 100):
    """List Risk Management / Listar Gestão de Risco"""
    return db.query(GestaoRisco).offset(skip).limit(limit).all()

@router.put("/id", response_model=GestaoRiscoRead)
def atualizar_gestao_risco(item_id: int, data: GestaoRiscoUpdate):
    """Update Risk Management / Atualizar Gestão de Risco"""
    item = db.query(GestaoRisco).filter(GestaoRisco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gestão de Risco não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
