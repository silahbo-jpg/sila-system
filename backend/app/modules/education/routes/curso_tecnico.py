from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.curso_tecnico import CursoTecnico
from app.modules.education.schemas.curso_tecnico import CursoTecnicoCreate, CursoTecnicoRead, CursoTecnicoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/curso-tecnico", tags=["Curso Técnico Municipal"])

@router.post("/", response_model=CursoTecnicoRead)
def criar_curso_tecnico(
    data: CursoTecnicoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Technical Course / Criar novo Curso Técnico Municipal"""
    db_item = CursoTecnico(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CursoTecnicoRead)
def obter_curso_tecnico(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Technical Course by ID / Obter Curso Técnico Municipal por ID"""
    item = db.query(CursoTecnico).filter(CursoTecnico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Curso Técnico Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CursoTecnicoRead])
def listar_curso_tecnico(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Technical Course / Listar Curso Técnico Municipal"""
    return db.query(CursoTecnico).filter(
        CursoTecnico.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CursoTecnicoRead)
def atualizar_curso_tecnico(
    item_id: int, 
    data: CursoTecnicoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Technical Course / Atualizar Curso Técnico Municipal"""
    item = db.query(CursoTecnico).filter(CursoTecnico.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Curso Técnico Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
