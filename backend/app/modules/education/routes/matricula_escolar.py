from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.matricula_escolar import MatriculaEscolar
from app.modules.education.schemas.matricula_escolar import MatriculaEscolarCreate, MatriculaEscolarRead, MatriculaEscolarUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/matricula-escolar", tags=["Matrícula Escolar"])

@router.post("/", response_model=MatriculaEscolarRead)
def criar_matricula_escolar(
    data: MatriculaEscolarCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new School Enrollment / Criar novo Matrícula Escolar"""
    db_item = MatriculaEscolar(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=MatriculaEscolarRead)
def obter_matricula_escolar(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get School Enrollment by ID / Obter Matrícula Escolar por ID"""
    item = db.query(MatriculaEscolar).filter(MatriculaEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Matrícula Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[MatriculaEscolarRead])
def listar_matricula_escolar(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List School Enrollment / Listar Matrícula Escolar"""
    return db.query(MatriculaEscolar).filter(
        MatriculaEscolar.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=MatriculaEscolarRead)
def atualizar_matricula_escolar(
    item_id: int, 
    data: MatriculaEscolarUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update School Enrollment / Atualizar Matrícula Escolar"""
    item = db.query(MatriculaEscolar).filter(MatriculaEscolar.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Matrícula Escolar não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
