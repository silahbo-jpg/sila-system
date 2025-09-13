from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.merenda_escolar import MerendaEscolar
from app.modules.education.schemas.merenda_escolar import MerendaEscolarCreate, MerendaEscolarRead, MerendaEscolarUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/merenda-escolar", tags=["Merenda Escolar"])

@router.post("/", response_model=MerendaEscolarRead)
def criar_merenda_escolar(
    data: MerendaEscolarCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new School Meals Program / Criar novo Merenda Escolar"""
    db_item = MerendaEscolar(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MerendaEscolarRead)
def obter_merenda_escolar(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get School Meals Program by ID / Obter Merenda Escolar por ID"""
    item = db.query(MerendaEscolar).filter(MerendaEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Merenda Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[MerendaEscolarRead])
def listar_merenda_escolar(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List School Meals Program / Listar Merenda Escolar"""
    return db.query(MerendaEscolar).filter(
        MerendaEscolar.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=MerendaEscolarRead)
def atualizar_merenda_escolar(
    item_id: int, 
    data: MerendaEscolarUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update School Meals Program / Atualizar Merenda Escolar"""
    item = db.query(MerendaEscolar).filter(MerendaEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Merenda Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
