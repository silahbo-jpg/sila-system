from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.registo_marca import RegistoMarca
from app.modules.commercial.schemas.registo_marca import RegistoMarcaCreate, RegistoMarcaRead, RegistoMarcaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-marca", tags=["Registo de Marca"])

@router.post("/", response_model=RegistoMarcaRead)
def criar_registo_marca(
    data: RegistoMarcaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Trademark Registration / Criar novo Registo de Marca"""
    db_item = RegistoMarca(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoMarcaRead)
def obter_registo_marca(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Trademark Registration by ID / Obter Registo de Marca por ID"""
    item = db.query(RegistoMarca).filter(RegistoMarca.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Marca não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoMarcaRead])
def listar_registo_marca(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Trademark Registration / Listar Registo de Marca"""
    return db.query(RegistoMarca).filter(
        RegistoMarca.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoMarcaRead)
def atualizar_registo_marca(
    item_id: int, 
    data: RegistoMarcaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Trademark Registration / Atualizar Registo de Marca"""
    item = db.query(RegistoMarca).filter(RegistoMarca.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Marca não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
