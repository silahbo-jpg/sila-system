from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.common.models.configuracao_global import ConfiguracaoGlobal
from app.modules.common.schemas.configuracao_global import ConfiguracaoGlobalCreate, ConfiguracaoGlobalRead, ConfiguracaoGlobalUpdate

router = APIRouter(prefix="/internal/configuracao-global", tags=["Configuração Global"])

@router.post("/", response_model=ConfiguracaoGlobalRead)
def criar_configuracao_global(data: ConfiguracaoGlobalCreate):
    """Create new Global Configuration / Criar novo Configuração Global"""
    db_item = ConfiguracaoGlobal(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ConfiguracaoGlobalRead)
def obter_configuracao_global(item_id: int):
    """Get Global Configuration by ID / Obter Configuração Global por ID"""
    item = db.query(ConfiguracaoGlobal).filter(ConfiguracaoGlobal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Configuração Global não encontrado")
    return item

@router.get("/", response_model=List[ConfiguracaoGlobalRead])
def listar_configuracao_global(skip: int = 0, limit: int = 100):
    """List Global Configuration / Listar Configuração Global"""
    return db.query(ConfiguracaoGlobal).offset(skip).limit(limit).all()

@router.put("/id", response_model=ConfiguracaoGlobalRead)
def atualizar_configuracao_global(item_id: int, data: ConfiguracaoGlobalUpdate):
    """Update Global Configuration / Atualizar Configuração Global"""
    item = db.query(ConfiguracaoGlobal).filter(ConfiguracaoGlobal.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Configuração Global não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
