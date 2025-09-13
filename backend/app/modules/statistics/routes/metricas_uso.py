from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.statistics.models.metricas_uso import MetricasUso
from app.modules.statistics.schemas.metricas_uso import MetricasUsoCreate, MetricasUsoRead, MetricasUsoUpdate

router = APIRouter(prefix="/internal/metricas-uso", tags=["Métricas de Uso"])

@router.post("/", response_model=MetricasUsoRead)
def criar_metricas_uso(data: MetricasUsoCreate):
    """Create new Usage Metrics / Criar novo Métricas de Uso"""
    db_item = MetricasUso(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MetricasUsoRead)
def obter_metricas_uso(item_id: int):
    """Get Usage Metrics by ID / Obter Métricas de Uso por ID"""
    item = db.query(MetricasUso).filter(MetricasUso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Métricas de Uso não encontrado")
    return item

@router.get("/", response_model=List[MetricasUsoRead])
def listar_metricas_uso(skip: int = 0, limit: int = 100):
    """List Usage Metrics / Listar Métricas de Uso"""
    return db.query(MetricasUso).offset(skip).limit(limit).all()

@router.put("/id", response_model=MetricasUsoRead)
def atualizar_metricas_uso(item_id: int, data: MetricasUsoUpdate):
    """Update Usage Metrics / Atualizar Métricas de Uso"""
    item = db.query(MetricasUso).filter(MetricasUso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Métricas de Uso não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
