from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.licenca_importacao import LicencaImportacao
from app.modules.commercial.schemas.licenca_importacao import LicencaImportacaoCreate, LicencaImportacaoRead, LicencaImportacaoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/licenca-importacao", tags=["Licença de Importação"])

@router.post("/", response_model=LicencaImportacaoRead)
def criar_licenca_importacao(
    data: LicencaImportacaoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Import License / Criar novo Licença de Importação"""
    db_item = LicencaImportacao(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=LicencaImportacaoRead)
def obter_licenca_importacao(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Import License by ID / Obter Licença de Importação por ID"""
    item = db.query(LicencaImportacao).filter(LicencaImportacao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Licença de Importação não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[LicencaImportacaoRead])
def listar_licenca_importacao(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Import License / Listar Licença de Importação"""
    return db.query(LicencaImportacao).filter(
        LicencaImportacao.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=LicencaImportacaoRead)
def atualizar_licenca_importacao(
    item_id: int, 
    data: LicencaImportacaoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Import License / Atualizar Licença de Importação"""
    item = db.query(LicencaImportacao).filter(LicencaImportacao.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Licença de Importação não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
