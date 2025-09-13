from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.registo_empresa import RegistoEmpresa
from app.modules.commercial.schemas.registo_empresa import RegistoEmpresaCreate, RegistoEmpresaRead, RegistoEmpresaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-empresa", tags=["Registo de Empresa"])

@router.post("/", response_model=RegistoEmpresaRead)
def criar_registo_empresa(
    data: RegistoEmpresaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Business Registration / Criar novo Registo de Empresa"""
    db_item = RegistoEmpresa(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoEmpresaRead)
def obter_registo_empresa(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Business Registration by ID / Obter Registo de Empresa por ID"""
    item = db.query(RegistoEmpresa).filter(RegistoEmpresa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Empresa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoEmpresaRead])
def listar_registo_empresa(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Business Registration / Listar Registo de Empresa"""
    return db.query(RegistoEmpresa).filter(
        RegistoEmpresa.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoEmpresaRead)
def atualizar_registo_empresa(
    item_id: int, 
    data: RegistoEmpresaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Business Registration / Atualizar Registo de Empresa"""
    item = db.query(RegistoEmpresa).filter(RegistoEmpresa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Empresa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
