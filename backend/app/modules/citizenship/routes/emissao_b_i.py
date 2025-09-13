from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.emissao_b_i import EmissaoBI
from app.modules.citizenship.schemas.emissao_b_i import EmissaoBICreate, EmissaoBIRead, EmissaoBIUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/emissao-b-i", tags=["Emissão de Bilhete de Identidade"])

@router.post("/", response_model=EmissaoBIRead)
def criar_emissao_b_i(
    data: EmissaoBICreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Identity Card Issuance / Criar novo Emissão de Bilhete de Identidade"""
    db_item = EmissaoBI(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EmissaoBIRead)
def obter_emissao_b_i(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Identity Card Issuance by ID / Obter Emissão de Bilhete de Identidade por ID"""
    item = db.query(EmissaoBI).filter(EmissaoBI.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Emissão de Bilhete de Identidade não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EmissaoBIRead])
def listar_emissao_b_i(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Identity Card Issuance / Listar Emissão de Bilhete de Identidade"""
    return db.query(EmissaoBI).filter(
        EmissaoBI.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EmissaoBIRead)
def atualizar_emissao_b_i(
    item_id: int, 
    data: EmissaoBIUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Identity Card Issuance / Atualizar Emissão de Bilhete de Identidade"""
    item = db.query(EmissaoBI).filter(EmissaoBI.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Emissão de Bilhete de Identidade não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
