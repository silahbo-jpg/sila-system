from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.statistics.models.analise_dados import AnaliseDados
from app.modules.statistics.schemas.analise_dados import AnaliseDadosCreate, AnaliseDadosRead, AnaliseDadosUpdate

router = APIRouter(prefix="/internal/analise-dados", tags=["Análise de Dados"])

@router.post("/", response_model=AnaliseDadosRead)
def criar_analise_dados(data: AnaliseDadosCreate):
    """Create new Data Analysis / Criar novo Análise de Dados"""
    db_item = AnaliseDados(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AnaliseDadosRead)
def obter_analise_dados(item_id: int):
    """Get Data Analysis by ID / Obter Análise de Dados por ID"""
    item = db.query(AnaliseDados).filter(AnaliseDados.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Análise de Dados não encontrado")
    return item

@router.get("/", response_model=List[AnaliseDadosRead])
def listar_analise_dados(skip: int = 0, limit: int = 100):
    """List Data Analysis / Listar Análise de Dados"""
    return db.query(AnaliseDados).offset(skip).limit(limit).all()

@router.put("/id", response_model=AnaliseDadosRead)
def atualizar_analise_dados(item_id: int, data: AnaliseDadosUpdate):
    """Update Data Analysis / Atualizar Análise de Dados"""
    item = db.query(AnaliseDados).filter(AnaliseDados.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Análise de Dados não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
