from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.fiscalizacao_mercado import FiscalizacaoMercado
from app.modules.commercial.schemas.fiscalizacao_mercado import FiscalizacaoMercadoCreate, FiscalizacaoMercadoRead, FiscalizacaoMercadoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/fiscalizacao-mercado", tags=["Fiscalização de Mercado"])

@router.post("/", response_model=FiscalizacaoMercadoRead)
def criar_fiscalizacao_mercado(
    data: FiscalizacaoMercadoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Market Inspection / Criar novo Fiscalização de Mercado"""
    db_item = FiscalizacaoMercado(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=FiscalizacaoMercadoRead)
def obter_fiscalizacao_mercado(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Market Inspection by ID / Obter Fiscalização de Mercado por ID"""
    item = db.query(FiscalizacaoMercado).filter(FiscalizacaoMercado.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Fiscalização de Mercado não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[FiscalizacaoMercadoRead])
def listar_fiscalizacao_mercado(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Market Inspection / Listar Fiscalização de Mercado"""
    return db.query(FiscalizacaoMercado).filter(
        FiscalizacaoMercado.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=FiscalizacaoMercadoRead)
def atualizar_fiscalizacao_mercado(
    item_id: int, 
    data: FiscalizacaoMercadoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Market Inspection / Atualizar Fiscalização de Mercado"""
    item = db.query(FiscalizacaoMercado).filter(FiscalizacaoMercado.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Fiscalização de Mercado não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
