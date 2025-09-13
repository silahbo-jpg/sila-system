from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.internal.models.otimizacao_performance import OtimizacaoPerformance
from app.modules.internal.schemas.otimizacao_performance import OtimizacaoPerformanceCreate, OtimizacaoPerformanceRead, OtimizacaoPerformanceUpdate

router = APIRouter(prefix="/internal/otimizacao-performance", tags=["Otimização de Performance"])

@router.post("/", response_model=OtimizacaoPerformanceRead)
def criar_otimizacao_performance(data: OtimizacaoPerformanceCreate):
    """Create new Performance Optimization / Criar novo Otimização de Performance"""
    db_item = OtimizacaoPerformance(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=OtimizacaoPerformanceRead)
def obter_otimizacao_performance(item_id: int):
    """Get Performance Optimization by ID / Obter Otimização de Performance por ID"""
    item = db.query(OtimizacaoPerformance).filter(OtimizacaoPerformance.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Otimização de Performance não encontrado")
    return item

@router.get("/", response_model=List[OtimizacaoPerformanceRead])
def listar_otimizacao_performance(skip: int = 0, limit: int = 100):
    """List Performance Optimization / Listar Otimização de Performance"""
    return db.query(OtimizacaoPerformance).offset(skip).limit(limit).all()

@router.put("/id", response_model=OtimizacaoPerformanceRead)
def atualizar_otimizacao_performance(item_id: int, data: OtimizacaoPerformanceUpdate):
    """Update Performance Optimization / Atualizar Otimização de Performance"""
    item = db.query(OtimizacaoPerformance).filter(OtimizacaoPerformance.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Otimização de Performance não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
