from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.address.models.geocodificacao_endereco import GeocodificacaoEndereco
from app.modules.address.schemas.geocodificacao_endereco import GeocodificacaoEnderecoCreate, GeocodificacaoEnderecoRead, GeocodificacaoEnderecoUpdate

router = APIRouter(prefix="/internal/geocodificacao-endereco", tags=["Geocodificação de Endereço"])

@router.post("/", response_model=GeocodificacaoEnderecoRead)
def criar_geocodificacao_endereco(data: GeocodificacaoEnderecoCreate):
    """Create new Address Geocoding / Criar novo Geocodificação de Endereço"""
    db_item = GeocodificacaoEndereco(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=GeocodificacaoEnderecoRead)
def obter_geocodificacao_endereco(item_id: int):
    """Get Address Geocoding by ID / Obter Geocodificação de Endereço por ID"""
    item = db.query(GeocodificacaoEndereco).filter(GeocodificacaoEndereco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Geocodificação de Endereço não encontrado")
    return item

@router.get("/", response_model=List[GeocodificacaoEnderecoRead])
def listar_geocodificacao_endereco(skip: int = 0, limit: int = 100):
    """List Address Geocoding / Listar Geocodificação de Endereço"""
    return db.query(GeocodificacaoEndereco).offset(skip).limit(limit).all()

@router.put("/id", response_model=GeocodificacaoEnderecoRead)
def atualizar_geocodificacao_endereco(item_id: int, data: GeocodificacaoEnderecoUpdate):
    """Update Address Geocoding / Atualizar Geocodificação de Endereço"""
    item = db.query(GeocodificacaoEndereco).filter(GeocodificacaoEndereco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Geocodificação de Endereço não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
