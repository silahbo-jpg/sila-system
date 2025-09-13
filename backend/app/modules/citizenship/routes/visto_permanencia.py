from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.visto_permanencia import VistoPermanencia
from app.modules.citizenship.schemas.visto_permanencia import VistoPermanenciaCreate, VistoPermanenciaRead, VistoPermanenciaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/visto-permanencia", tags=["Visto de Permanência"])

@router.post("/", response_model=VistoPermanenciaRead)
def criar_visto_permanencia(
    data: VistoPermanenciaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Permanent Residence Visa / Criar novo Visto de Permanência"""
    db_item = VistoPermanencia(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=VistoPermanenciaRead)
def obter_visto_permanencia(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Permanent Residence Visa by ID / Obter Visto de Permanência por ID"""
    item = db.query(VistoPermanencia).filter(VistoPermanencia.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Visto de Permanência não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[VistoPermanenciaRead])
def listar_visto_permanencia(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Permanent Residence Visa / Listar Visto de Permanência"""
    return db.query(VistoPermanencia).filter(
        VistoPermanencia.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=VistoPermanenciaRead)
def atualizar_visto_permanencia(
    item_id: int, 
    data: VistoPermanenciaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Permanent Residence Visa / Atualizar Visto de Permanência"""
    item = db.query(VistoPermanencia).filter(VistoPermanencia.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Visto de Permanência não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
