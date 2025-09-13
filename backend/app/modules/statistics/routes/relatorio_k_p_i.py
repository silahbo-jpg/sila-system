from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.statistics.models.relatorio_k_p_i import RelatorioKPI
from app.modules.statistics.schemas.relatorio_k_p_i import RelatorioKPICreate, RelatorioKPIRead, RelatorioKPIUpdate

router = APIRouter(prefix="/internal/relatorio-k-p-i", tags=["Relatório de KPI"])

@router.post("/", response_model=RelatorioKPIRead)
def criar_relatorio_k_p_i(data: RelatorioKPICreate):
    """Create new KPI Report / Criar novo Relatório de KPI"""
    db_item = RelatorioKPI(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RelatorioKPIRead)
def obter_relatorio_k_p_i(item_id: int):
    """Get KPI Report by ID / Obter Relatório de KPI por ID"""
    item = db.query(RelatorioKPI).filter(RelatorioKPI.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Relatório de KPI não encontrado")
    return item

@router.get("/", response_model=List[RelatorioKPIRead])
def listar_relatorio_k_p_i(skip: int = 0, limit: int = 100):
    """List KPI Report / Listar Relatório de KPI"""
    return db.query(RelatorioKPI).offset(skip).limit(limit).all()

@router.put("/id", response_model=RelatorioKPIRead)
def atualizar_relatorio_k_p_i(item_id: int, data: RelatorioKPIUpdate):
    """Update KPI Report / Atualizar Relatório de KPI"""
    item = db.query(RelatorioKPI).filter(RelatorioKPI.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Relatório de KPI não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
