from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.declaracao_residencia import DeclaracaoResidencia
from app.modules.citizenship.schemas.declaracao_residencia import DeclaracaoResidenciaCreate, DeclaracaoResidenciaRead, DeclaracaoResidenciaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/declaracao-residencia", tags=["Declaração de Residência"])

@router.post("/", response_model=DeclaracaoResidenciaRead)
def criar_declaracao_residencia(
    data: DeclaracaoResidenciaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Residence Declaration / Criar novo Declaração de Residência"""
    db_item = DeclaracaoResidencia(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=DeclaracaoResidenciaRead)
def obter_declaracao_residencia(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Residence Declaration by ID / Obter Declaração de Residência por ID"""
    item = db.query(DeclaracaoResidencia).filter(DeclaracaoResidencia.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Declaração de Residência não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[DeclaracaoResidenciaRead])
def listar_declaracao_residencia(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Residence Declaration / Listar Declaração de Residência"""
    return db.query(DeclaracaoResidencia).filter(
        DeclaracaoResidencia.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=DeclaracaoResidenciaRead)
def atualizar_declaracao_residencia(
    item_id: int, 
    data: DeclaracaoResidenciaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Residence Declaration / Atualizar Declaração de Residência"""
    item = db.query(DeclaracaoResidencia).filter(DeclaracaoResidencia.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Declaração de Residência não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
