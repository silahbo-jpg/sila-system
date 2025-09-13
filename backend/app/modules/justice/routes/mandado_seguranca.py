from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.mandado_seguranca import MandadoSeguranca
from app.modules.justice.schemas.mandado_seguranca import MandadoSegurancaCreate, MandadoSegurancaRead, MandadoSegurancaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/mandado-seguranca", tags=["Mandado de Segurança"])

@router.post("/", response_model=MandadoSegurancaRead)
def criar_mandado_seguranca(
    data: MandadoSegurancaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Security Order / Criar novo Mandado de Segurança"""
    db_item = MandadoSeguranca(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MandadoSegurancaRead)
def obter_mandado_seguranca(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Security Order by ID / Obter Mandado de Segurança por ID"""
    item = db.query(MandadoSeguranca).filter(MandadoSeguranca.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Mandado de Segurança não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[MandadoSegurancaRead])
def listar_mandado_seguranca(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Security Order / Listar Mandado de Segurança"""
    return db.query(MandadoSeguranca).filter(
        MandadoSeguranca.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=MandadoSegurancaRead)
def atualizar_mandado_seguranca(
    item_id: int, 
    data: MandadoSegurancaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Security Order / Atualizar Mandado de Segurança"""
    item = db.query(MandadoSeguranca).filter(MandadoSeguranca.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Mandado de Segurança não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
