from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.emissao_passaporte import EmissaoPassaporte
from app.modules.citizenship.schemas.emissao_passaporte import EmissaoPassaporteCreate, EmissaoPassaporteRead, EmissaoPassaporteUpdate
from app.core.auth.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/emissao-passaporte", tags=["Emissão de Passaporte"])

@router.post("/", response_model=EmissaoPassaporteRead)
def criar_emissao_passaporte(
    data: EmissaoPassaporteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Passport Issuance / Criar novo Emissão de Passaporte"""
    db_item = EmissaoPassaporte(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=EmissaoPassaporteRead)
def obter_emissao_passaporte(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Passport Issuance by ID / Obter Emissão de Passaporte por ID"""
    item = db.query(EmissaoPassaporte).filter(EmissaoPassaporte.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Emissão de Passaporte não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[EmissaoPassaporteRead])
def listar_emissao_passaporte(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Passport Issuance / Listar Emissão de Passaporte"""
    return db.query(EmissaoPassaporte).filter(
        EmissaoPassaporte.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=EmissaoPassaporteRead)
def atualizar_emissao_passaporte(
    item_id: int, 
    data: EmissaoPassaporteUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Passport Issuance / Atualizar Emissão de Passaporte"""
    item = db.query(EmissaoPassaporte).filter(EmissaoPassaporte.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Emissão de Passaporte não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
