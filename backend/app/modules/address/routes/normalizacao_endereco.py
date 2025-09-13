from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.address.models.normalizacao_endereco import NormalizacaoEndereco
from app.modules.address.schemas.normalizacao_endereco import NormalizacaoEnderecoCreate, NormalizacaoEnderecoRead, NormalizacaoEnderecoUpdate

router = APIRouter(prefix="/internal/normalizacao-endereco", tags=["Normalização de Endereço"])

@router.post("/", response_model=NormalizacaoEnderecoRead)
def criar_normalizacao_endereco(data: NormalizacaoEnderecoCreate):
    """Create new Address Normalization / Criar novo Normalização de Endereço"""
    db_item = NormalizacaoEndereco(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=NormalizacaoEnderecoRead)
def obter_normalizacao_endereco(item_id: int):
    """Get Address Normalization by ID / Obter Normalização de Endereço por ID"""
    item = db.query(NormalizacaoEndereco).filter(NormalizacaoEndereco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Normalização de Endereço não encontrado")
    return item

@router.get("/", response_model=List[NormalizacaoEnderecoRead])
def listar_normalizacao_endereco(skip: int = 0, limit: int = 100):
    """List Address Normalization / Listar Normalização de Endereço"""
    return db.query(NormalizacaoEndereco).offset(skip).limit(limit).all()

@router.put("/id", response_model=NormalizacaoEnderecoRead)
def atualizar_normalizacao_endereco(item_id: int, data: NormalizacaoEnderecoUpdate):
    """Update Address Normalization / Atualizar Normalização de Endereço"""
    item = db.query(NormalizacaoEndereco).filter(NormalizacaoEndereco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Normalização de Endereço não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
