from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.common.models.cache_distribuido import CacheDistribuido
from app.modules.common.schemas.cache_distribuido import CacheDistribuidoCreate, CacheDistribuidoRead, CacheDistribuidoUpdate

router = APIRouter(prefix="/internal/cache-distribuido", tags=["Cache Distribuído"])

@router.post("/", response_model=CacheDistribuidoRead)
def criar_cache_distribuido(data: CacheDistribuidoCreate):
    """Create new Distributed Cache / Criar novo Cache Distribuído"""
    db_item = CacheDistribuido(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CacheDistribuidoRead)
def obter_cache_distribuido(item_id: int):
    """Get Distributed Cache by ID / Obter Cache Distribuído por ID"""
    item = db.query(CacheDistribuido).filter(CacheDistribuido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cache Distribuído não encontrado")
    return item

@router.get("/", response_model=List[CacheDistribuidoRead])
def listar_cache_distribuido(skip: int = 0, limit: int = 100):
    """List Distributed Cache / Listar Cache Distribuído"""
    return db.query(CacheDistribuido).offset(skip).limit(limit).all()

@router.put("/id", response_model=CacheDistribuidoRead)
def atualizar_cache_distribuido(item_id: int, data: CacheDistribuidoUpdate):
    """Update Distributed Cache / Atualizar Cache Distribuído"""
    item = db.query(CacheDistribuido).filter(CacheDistribuido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cache Distribuído não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
