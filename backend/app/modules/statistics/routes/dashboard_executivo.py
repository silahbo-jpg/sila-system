from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.statistics.models.dashboard_executivo import DashboardExecutivo
from app.modules.statistics.schemas.dashboard_executivo import DashboardExecutivoCreate, DashboardExecutivoRead, DashboardExecutivoUpdate

router = APIRouter(prefix="/internal/dashboard-executivo", tags=["Dashboard Executivo"])

@router.post("/", response_model=DashboardExecutivoRead)
def criar_dashboard_executivo(data: DashboardExecutivoCreate):
    """Create new Executive Dashboard / Criar novo Dashboard Executivo"""
    db_item = DashboardExecutivo(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=DashboardExecutivoRead)
def obter_dashboard_executivo(item_id: int):
    """Get Executive Dashboard by ID / Obter Dashboard Executivo por ID"""
    item = db.query(DashboardExecutivo).filter(DashboardExecutivo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Dashboard Executivo não encontrado")
    return item

@router.get("/", response_model=List[DashboardExecutivoRead])
def listar_dashboard_executivo(skip: int = 0, limit: int = 100):
    """List Executive Dashboard / Listar Dashboard Executivo"""
    return db.query(DashboardExecutivo).offset(skip).limit(limit).all()

@router.put("/id", response_model=DashboardExecutivoRead)
def atualizar_dashboard_executivo(item_id: int, data: DashboardExecutivoUpdate):
    """Update Executive Dashboard / Atualizar Dashboard Executivo"""
    item = db.query(DashboardExecutivo).filter(DashboardExecutivo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Dashboard Executivo não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
