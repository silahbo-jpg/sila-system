from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.atualizacao_endereco import AtualizacaoEndereco
from app.modules.citizenship.schemas.atualizacao_endereco import AtualizacaoEnderecoCreate, AtualizacaoEnderecoRead, AtualizacaoEnderecoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/atualizacao-endereco", tags=["Atualização de Endereço"])

@router.post("/", response_model=AtualizacaoEnderecoRead)
def criar_atualizacao_endereco(
    data: AtualizacaoEnderecoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Address Update / Criar novo Atualização de Endereço"""
    db_item = AtualizacaoEndereco(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AtualizacaoEnderecoRead)
def obter_atualizacao_endereco(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Address Update by ID / Obter Atualização de Endereço por ID"""
    item = db.query(AtualizacaoEndereco).filter(AtualizacaoEndereco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Atualização de Endereço não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AtualizacaoEnderecoRead])
def listar_atualizacao_endereco(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Address Update / Listar Atualização de Endereço"""
    return db.query(AtualizacaoEndereco).filter(
        AtualizacaoEndereco.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AtualizacaoEnderecoRead)
def atualizar_atualizacao_endereco(
    item_id: int, 
    data: AtualizacaoEnderecoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Address Update / Atualizar Atualização de Endereço"""
    item = db.query(AtualizacaoEndereco).filter(AtualizacaoEndereco.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Atualização de Endereço não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
