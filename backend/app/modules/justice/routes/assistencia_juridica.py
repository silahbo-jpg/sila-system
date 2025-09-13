from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.assistencia_juridica import AssistenciaJuridica
from app.modules.justice.schemas.assistencia_juridica import AssistenciaJuridicaCreate, AssistenciaJuridicaRead, AssistenciaJuridicaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/assistencia-juridica", tags=["Assistência Jurídica Gratuita"])

@router.post("/", response_model=AssistenciaJuridicaRead)
def criar_assistencia_juridica(
    data: AssistenciaJuridicaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Free Legal Assistance / Criar novo Assistência Jurídica Gratuita"""
    db_item = AssistenciaJuridica(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AssistenciaJuridicaRead)
def obter_assistencia_juridica(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Free Legal Assistance by ID / Obter Assistência Jurídica Gratuita por ID"""
    item = db.query(AssistenciaJuridica).filter(AssistenciaJuridica.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assistência Jurídica Gratuita não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AssistenciaJuridicaRead])
def listar_assistencia_juridica(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Free Legal Assistance / Listar Assistência Jurídica Gratuita"""
    return db.query(AssistenciaJuridica).filter(
        AssistenciaJuridica.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AssistenciaJuridicaRead)
def atualizar_assistencia_juridica(
    item_id: int, 
    data: AssistenciaJuridicaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Free Legal Assistance / Atualizar Assistência Jurídica Gratuita"""
    item = db.query(AssistenciaJuridica).filter(AssistenciaJuridica.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assistência Jurídica Gratuita não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
