from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.finance.models.apoio_empreendedor import ApoioEmpreendedor
from app.modules.finance.schemas.apoio_empreendedor import ApoioEmpreendedorCreate, ApoioEmpreendedorRead, ApoioEmpreendedorUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/apoio-empreendedor", tags=["Apoio ao Empreendedor"])

@router.post("/", response_model=ApoioEmpreendedorRead)
def criar_apoio_empreendedor(
    data: ApoioEmpreendedorCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Entrepreneur Support / Criar novo Apoio ao Empreendedor"""
    db_item = ApoioEmpreendedor(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ApoioEmpreendedorRead)
def obter_apoio_empreendedor(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Entrepreneur Support by ID / Obter Apoio ao Empreendedor por ID"""
    item = db.query(ApoioEmpreendedor).filter(ApoioEmpreendedor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Apoio ao Empreendedor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ApoioEmpreendedorRead])
def listar_apoio_empreendedor(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Entrepreneur Support / Listar Apoio ao Empreendedor"""
    return db.query(ApoioEmpreendedor).filter(
        ApoioEmpreendedor.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ApoioEmpreendedorRead)
def atualizar_apoio_empreendedor(
    item_id: int, 
    data: ApoioEmpreendedorUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Entrepreneur Support / Atualizar Apoio ao Empreendedor"""
    item = db.query(ApoioEmpreendedor).filter(ApoioEmpreendedor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Apoio ao Empreendedor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
