from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.urbanism.models.sinalizacao_trafego import SinalizacaoTrafego
from app.modules.urbanism.schemas.sinalizacao_trafego import SinalizacaoTrafegoCreate, SinalizacaoTrafegoRead, SinalizacaoTrafegoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/sinalizacao-trafego", tags=["Sinalização de Tráfego"])

@router.post("/", response_model=SinalizacaoTrafegoRead)
def criar_sinalizacao_trafego(
    data: SinalizacaoTrafegoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Traffic Signage / Criar novo Sinalização de Tráfego"""
    db_item = SinalizacaoTrafego(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=SinalizacaoTrafegoRead)
def obter_sinalizacao_trafego(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Traffic Signage by ID / Obter Sinalização de Tráfego por ID"""
    item = db.query(SinalizacaoTrafego).filter(SinalizacaoTrafego.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sinalização de Tráfego não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[SinalizacaoTrafegoRead])
def listar_sinalizacao_trafego(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Traffic Signage / Listar Sinalização de Tráfego"""
    return db.query(SinalizacaoTrafego).filter(
        SinalizacaoTrafego.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=SinalizacaoTrafegoRead)
def atualizar_sinalizacao_trafego(
    item_id: int, 
    data: SinalizacaoTrafegoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Traffic Signage / Atualizar Sinalização de Tráfego"""
    item = db.query(SinalizacaoTrafego).filter(SinalizacaoTrafego.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sinalização de Tráfego não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
